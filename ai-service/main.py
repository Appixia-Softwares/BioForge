from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import torch
import esm
import numpy as np
from Bio.Seq import Seq
from Bio.PDB import PDBParser, PDBIO
import os
import tempfile
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="BioForge AI Service",
    description="AI service for the BioForge synthetic biology platform",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request models
class DNASequence(BaseModel):
    sequence: str
    name: Optional[str] = None

class ProteinSequence(BaseModel):
    sequence: str
    name: Optional[str] = None

# Load ESM-2 model
try:
    logger.info("Loading ESM-2 model...")
    model, alphabet = esm.pretrained.esm2_t33_650M_UR50D()
    model.eval()  # Set the model to evaluation mode
    
    # Check if CUDA is available
    if torch.cuda.is_available():
        model = model.cuda()
        logger.info("ESM-2 model loaded on GPU")
    else:
        logger.info("ESM-2 model loaded on CPU")
    
    # Load ESMFold for structure prediction
    try:
        esmfold = esm.pretrained.esmfold_v1()
        esmfold.eval()
        
        if torch.cuda.is_available():
            esmfold = esmfold.cuda()
            logger.info("ESMFold model loaded on GPU")
        else:
            logger.info("ESMFold model loaded on CPU")
    except Exception as e:
        logger.error(f"Error loading ESMFold model: {e}")
        esmfold = None
        logger.warning("Structure prediction will not be available")
    
    model_loaded = True
except Exception as e:
    logger.error(f"Error loading ESM-2 model: {e}")
    model_loaded = False
    logger.warning("AI service will run in simulation mode")

# Helper functions
def dna_to_protein(dna_sequence: str) -> str:
    """Convert DNA sequence to protein sequence."""
    seq = Seq(dna_sequence.upper())
    return str(seq.translate())

def find_orfs(dna_sequence: str, min_length: int = 30) -> List[str]:
    """Find all open reading frames in a DNA sequence."""
    seq = Seq(dna_sequence.upper())
    orfs = []
    
    # Check all reading frames
    for frame in range(3):
        # Get the sequence in this reading frame
        frame_seq = seq[frame:]
        
        # Adjust length to be divisible by 3
        frame_seq = frame_seq[:len(frame_seq) - (len(frame_seq) % 3)]
        
        # Find start codons
        for i in range(0, len(frame_seq), 3):
            if frame_seq[i:i+3] == "ATG":
                # Found a start codon, look for a stop codon
                for j in range(i, len(frame_seq), 3):
                    if frame_seq[j:j+3] in ["TAA", "TAG", "TGA"]:
                        # Found a stop codon, extract the ORF
                        orf = frame_seq[i:j+3]
                        if len(orf) >= min_length:  # Minimum length for a meaningful ORF
                            orfs.append(str(orf))
                        break
    
    return orfs

# API endpoints
@app.get("/")
async def root():
    """Root endpoint to check if the service is running."""
    return {"message": "BioForge AI Service is running", "model_loaded": model_loaded}

@app.post("/api/validate")
async def validate_sequence(sequence: DNASequence):
    """Validate a DNA sequence."""
    logger.info(f"Validating sequence: {sequence.name or 'unnamed'}")
    
    # Check for valid DNA characters
    valid_chars = set("ATGC")
    invalid_chars = [char for char in sequence.sequence.upper() if char not in valid_chars]
    
    if invalid_chars:
        return {
            "valid": False,
            "issues": [f"Invalid DNA characters found: {', '.join(set(invalid_chars))}"],
            "warnings": [],
            "suggestions": ["Replace invalid characters with A, T, G, or C"]
        }
    
    # Find ORFs
    orfs = find_orfs(sequence.sequence)
    
    # Check for potential issues
    issues = []
    warnings = []
    suggestions = []
    
    # Check for homopolymers (runs of the same nucleotide)
    homopolymers = []
    for base in "ATGC":
        pattern = base * 6  # Look for runs of 6 or more
        if pattern in sequence.sequence.upper():
            homopolymers.append(f"{base}x6+")
    
    if homopolymers:
        warnings.append(f"Homopolymer regions found: {', '.join(homopolymers)}")
        suggestions.append("Consider breaking up homopolymer regions to improve stability")
    
    # Check GC content
    gc_count = sequence.sequence.upper().count("G") + sequence.sequence.upper().count("C")
    gc_content = gc_count / len(sequence.sequence) if len(sequence.sequence) > 0 else 0
    
    if gc_content < 0.3:
        warnings.append(f"Low GC content ({gc_content:.2f})")
        suggestions.append("Consider increasing GC content for stability")
    elif gc_content > 0.7:
        warnings.append(f"High GC content ({gc_content:.2f})")
        suggestions.append("Consider decreasing GC content for easier handling")
    
    # Check for rare codons if ORFs are found
    if orfs:
        # E. coli rare codons
        rare_codons = ["CTA", "ATA", "CGA", "CGG", "AGG", "AGA", "CCC", "TCG"]
        rare_codons_found = []
        
        for orf in orfs:
            for i in range(0, len(orf), 3):
                codon = orf[i:i+3]
                if codon in rare_codons and codon not in rare_codons_found:
                    rare_codons_found.append(codon)
        
        if rare_codons_found:
            warnings.append(f"Rare codons found: {', '.join(rare_codons_found)}")
            suggestions.append("Consider codon optimization to improve expression")
    else:
        warnings.append("No open reading frames found")
        suggestions.append("Check if this is intentional or if there's a frameshift")
    
    return {
        "valid": True,
        "sequence_length": len(sequence.sequence),
        "gc_content": gc_content,
        "orfs": len(orfs),
        "issues": issues,
        "warnings": warnings,
        "suggestions": suggestions
    }

@app.post("/api/predict")
async def predict_function(sequence: DNASequence):
    """Predict the function of a DNA sequence."""
    logger.info(f"Predicting function for sequence: {sequence.name or 'unnamed'}")
    
    # Find ORFs
    orfs = find_orfs(sequence.sequence)
    
    if not orfs:
        return {
            "prediction": "Unknown",
            "confidence": 0.0,
            "possible_functions": [],
            "protein_domains": [],
            "notes": ["No open reading frames found"]
        }
    
    # Use the longest ORF for prediction
    longest_orf = max(orfs, key=len)
    protein_seq = str(Seq(longest_orf).translate())
    
    # If the model is not loaded, return simulated results
    if not model_loaded:
        return _simulate_prediction(sequence.sequence)
    
    # Prepare the sequence for ESM-2
    data = [(f"protein_{hash(protein_seq)}", protein_seq)]
    batch_converter = alphabet.get_batch_converter()
    batch_labels, batch_strs, batch_tokens = batch_converter(data)
    
    # Move to GPU if available
    if torch.cuda.is_available():
        batch_tokens = batch_tokens.cuda()
    
    # Get embeddings
    with torch.no_grad():
        results = model(batch_tokens, repr_layers=[33], return_contacts=True)
    token_representations = results["representations"][33]
    
    # Use the [CLS] token representation for classification
    cls_representation = token_representations[0, 0, :].cpu().numpy()
    
    # In a real implementation, you would use a trained classifier
    # For now, we'll use a simulated prediction
    return _simulate_prediction(sequence.sequence, cls_representation)

@app.post("/api/structure")
async def predict_structure(protein: ProteinSequence):
    """Predict the 3D structure of a protein sequence."""
    logger.info(f"Predicting structure for protein: {protein.name or 'unnamed'}")
    
    if not model_loaded or esmfold is None:
        raise HTTPException(status_code=503, detail="Structure prediction model not available")
    
    # Check if the sequence is too long
    if len(protein.sequence) > 1000:
        raise HTTPException(status_code=400, detail="Protein sequence too long (max 1000 amino acids)")
    
    # Predict the structure
    with torch.no_grad():
        output = esmfold.infer_pdb(protein.sequence)
    
    # Create a temporary file to save the PDB
    with tempfile.NamedTemporaryFile(suffix=".pdb", delete=False) as tmp:
        tmp.write(output.encode())
        tmp_path = tmp.name
    
    # Parse the PDB file to extract information
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("protein", tmp_path)
    
    # Extract information from the structure
    residue_count = sum(1 for _ in structure.get_residues())
    atom_count = sum(1 for _ in structure.get_atoms())
    
    # Clean up the temporary file
    os.unlink(tmp_path)
    
    return {
        "pdb_data": output,
        "residue_count": residue_count,
        "atom_count": atom_count,
        "sequence_length": len(protein.sequence)
    }

@app.post("/api/toxicity")
async def predict_toxicity(protein: ProteinSequence):
    """Predict the toxicity of a protein sequence."""
    logger.info(f"Predicting toxicity for protein: {protein.name or 'unnamed'}")
    
    # In a real implementation, you would use a trained toxicity predictor
    # For now, we'll use a simulated prediction
    
    # Check for known toxic motifs (simplified example)
    toxic_motifs = ["RRRR", "KKKK", "DDDD", "EEEE"]
    found_motifs = []
    
    for motif in toxic_motifs:
        if motif in protein.sequence:
            found_motifs.append(motif)
    
    # Calculate a toxicity score (simplified)
    base_score = 0.1  # Base toxicity score
    
    if found_motifs:
        base_score += 0.2 * len(found_motifs)
    
    # Check for unusual amino acid composition
    aa_counts = {}
    for aa in protein.sequence:
        aa_counts[aa] = aa_counts.get(aa, 0) + 1
    
    # Check for high content of specific amino acids
    for aa, count in aa_counts.items():
        if count / len(protein.sequence) > 0.2:  # If any amino acid is >20% of the sequence
            base_score += 0.1
    
    # Ensure the score is between 0 and 1
    toxicity_score = min(1.0, max(0.0, base_score))
    
    return {
        "toxicity_score": toxicity_score,
        "toxic_motifs": found_motifs,
        "risk_level": "High" if toxicity_score > 0.7 else "Medium" if toxicity_score > 0.3 else "Low",
        "notes": [
            "This is a preliminary toxicity assessment",
            "Further experimental validation is recommended"
        ]
    }

def _simulate_prediction(dna_sequence: str, embedding=None) -> Dict[str, Any]:
    """Simulate a prediction for demonstration purposes."""
    # Calculate some features from the sequence
    seq = dna_sequence.upper()
    length = len(seq)
    gc_content = (seq.count("G") + seq.count("C")) / length if length > 0 else 0
    
    # Simulate different predictions based on sequence characteristics
    if "ATG" in seq and any(stop in seq for stop in ["TAA", "TAG", "TGA"]):
        # Looks like it has start and stop codons
        if "ATGGTGAGCAAGGGCGAGGAG" in seq:  # GFP start
            return {
                "prediction": "Green Fluorescent Protein (GFP)",
                "confidence": 0.95,
                "possible_functions": ["Fluorescent reporter", "Protein tagging"],
                "protein_domains": ["GFP beta-barrel"],
                "notes": ["High confidence match to GFP sequence"]
            }
        elif "ATGGCCTCCTCCGAGGACGTC" in seq:  # RFP start
            return {
                "prediction": "Red Fluorescent Protein (RFP)",
                "confidence": 0.92,
                "possible_functions": ["Fluorescent reporter", "Protein tagging"],
                "protein_domains": ["DsRed-like"],
                "notes": ["High confidence match to RFP sequence"]
            }
        elif gc_content > 0.65:
            return {
                "prediction": "Stress Response Protein",
                "confidence": 0.78,
                "possible_functions": ["Heat shock response", "Oxidative stress response"],
                "protein_domains": ["Chaperone-like", "Redox-active"],
                "notes": ["High GC content suggests stress-related function"]
            }
        else:
            return {
                "prediction": "Metabolic Enzyme",
                "confidence": 0.65,
                "possible_functions": ["Carbon metabolism", "Biosynthesis"],
                "protein_domains": ["Enzyme active site", "Substrate binding domain"],
                "notes": ["Sequence contains features consistent with metabolic enzymes"]
            }
    elif "TATAAT" in seq or "TTGACA" in seq:  # Common promoter elements
        return {
            "prediction": "Promoter Region",
            "confidence": 0.88,
            "possible_functions": ["Transcription initiation", "Gene regulation"],
            "protein_domains": [],
            "notes": ["Contains sigma-70 promoter consensus sequences"]
        }
    elif gc_content < 0.4 and length < 50:
        return {
            "prediction": "Ribosome Binding Site",
            "confidence": 0.75,
            "possible_functions": ["Translation initiation"],
            "protein_domains": [],
            "notes": ["Low GC content and short length typical of RBS"]
        }
    else:
        return {
            "prediction": "Unknown Function",
            "confidence": 0.3,
            "possible_functions": ["Structural element", "Regulatory element", "Coding sequence"],
            "protein_domains": [],
            "notes": ["Sequence does not match known patterns"]
        }

# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
