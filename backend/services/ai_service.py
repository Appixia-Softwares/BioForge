from typing import Dict, Any
import torch
import esm
import numpy as np
from Bio.Seq import Seq
from Bio.Data import CodonTable
import os
import time

class AIService:
    def __init__(self):
        # Load ESM-2 model
        self.model_loaded = False
        self.cache = {}  # Simple in-memory cache
        self.cache_expiry = 3600  # Cache expiry in seconds (1 hour)
        
        # Try to load the model
        try:
            # Load the ESM-2 model
            self.model, self.alphabet = esm.pretrained.esm2_t33_650M_UR50D()
            self.model.eval()  # Set the model to evaluation mode
            
            # Check if CUDA is available
            if torch.cuda.is_available():
                self.model = self.model.cuda()
                print("ESM-2 model loaded on GPU")
            else:
                print("ESM-2 model loaded on CPU")
            
            self.model_loaded = True
        except Exception as e:
            print(f"Error loading ESM-2 model: {e}")
            print("AI service will run in simulation mode")
    
    def validate_sequence(self, dna_sequence: str) -> Dict[str, Any]:
        """
        Validate a DNA sequence using the AI service.
        Check for:
        - Valid DNA characters (A, T, G, C)
        - Open reading frames
        - Potential issues (e.g., rare codons, homopolymers)
        """
        # Check cache
        cache_key = f"validate_{dna_sequence}"
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if time.time() - cache_entry["timestamp"] < self.cache_expiry:
                return cache_entry["data"]
        
        # Check for valid DNA characters
        valid_chars = set("ATGC")
        invalid_chars = [char for char in dna_sequence.upper() if char not in valid_chars]
        
        if invalid_chars:
            result = {
                "valid": False,
                "issues": [f"Invalid DNA characters found: {', '.join(set(invalid_chars))}"],
                "warnings": [],
                "suggestions": ["Replace invalid characters with A, T, G, or C"]
            }
            
            # Cache the result
            self.cache[cache_key] = {
                "data": result,
                "timestamp": time.time()
            }
            
            return result
        
        # Check for open reading frames
        seq = Seq(dna_sequence.upper())
        orfs = self._find_orfs(seq)
        
        # Check for potential issues
        issues = []
        warnings = []
        suggestions = []
        
        # Check for homopolymers (runs of the same nucleotide)
        homopolymers = self._find_homopolymers(dna_sequence.upper())
        if homopolymers:
            warnings.append(f"Homopolymer regions found: {', '.join(homopolymers)}")
            suggestions.append("Consider breaking up homopolymer regions to improve stability")
        
        # Check for rare codons if ORFs are found
        if orfs:
            rare_codons = self._check_rare_codons(seq)
            if rare_codons:
                warnings.append(f"Rare codons found: {', '.join(rare_codons)}")
                suggestions.append("Consider codon optimization to improve expression")
        else:
            warnings.append("No open reading frames found")
            suggestions.append("Check if this is intentional or if there's a frameshift")
        
        # Check GC content
        gc_content = self._calculate_gc_content(dna_sequence.upper())
        if gc_content < 0.3:
            warnings.append(f"Low GC content ({gc_content:.2f})")
            suggestions.append("Consider increasing GC content for stability")
        elif gc_content > 0.7:
            warnings.append(f"High GC content ({gc_content:.2f})")
            suggestions.append("Consider decreasing GC content for easier handling")
        
        result = {
            "valid": True,
            "sequence_length": len(dna_sequence),
            "gc_content": gc_content,
            "orfs": len(orfs),
            "issues": issues,
            "warnings": warnings,
            "suggestions": suggestions
        }
        
        # Cache the result
        self.cache[cache_key] = {
            "data": result,
            "timestamp": time.time()
        }
        
        return result
    
    def predict_function(self, dna_sequence: str) -> Dict[str, Any]:
        """
        Predict the function of a DNA sequence using the AI service.
        """
        # Check cache
        cache_key = f"predict_{dna_sequence}"
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if time.time() - cache_entry["timestamp"] < self.cache_expiry:
                return cache_entry["data"]
        
        # If the model is not loaded, return simulated results
        if not self.model_loaded:
            result = self._simulate_prediction(dna_sequence)
            
            # Cache the result
            self.cache[cache_key] = {
                "data": result,
                "timestamp": time.time()
            }
            
            return result
        
        # Convert DNA to protein sequence
        seq = Seq(dna_sequence.upper())
        orfs = self._find_orfs(seq)
        
        if not orfs:
            result = {
                "prediction": "Unknown",
                "confidence": 0.0,
                "possible_functions": [],
                "protein_domains": [],
                "notes": ["No open reading frames found"]
            }
            
            # Cache the result
            self.cache[cache_key] = {
                "data": result,
                "timestamp": time.time()
            }
            
            return result
        
        # Use the longest ORF for prediction
        longest_orf = max(orfs, key=lambda x: len(x))
        protein_seq = longest_orf.translate()
        
        # Prepare the sequence for ESM-2
        data = [(f"protein_{hash(str(protein_seq))}", str(protein_seq))]
        batch_converter = self.alphabet.get_batch_converter()
        batch_labels, batch_strs, batch_tokens = batch_converter(data)
        
        # Move to GPU if available
        if torch.cuda.is_available():
            batch_tokens = batch_tokens.cuda()
        
        # Get embeddings
        with torch.no_grad():
            results = self.model(batch_tokens, repr_layers=[33], return_contacts=True)
        token_representations = results["representations"][33]
        
        # Use the [CLS] token representation for classification
        cls_representation = token_representations[0, 0, :].cpu().numpy()
        
        # Simulate classification based on the embedding
        # In a real implementation, you would use a trained classifier
        result = self._simulate_prediction(dna_sequence, cls_representation)
        
        # Cache the result
        self.cache[cache_key] = {
            "data": result,
            "timestamp": time.time()
        }
        
        return result
    
    def _find_orfs(self, seq):
        """
        Find all open reading frames in a DNA sequence.
        """
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
                            if len(orf) >= 30:  # Minimum length for a meaningful ORF
                                orfs.append(orf)
                            break
        
        return orfs
    
    def _find_homopolymers(self, seq, min_length=6):
        """
        Find homopolymer regions in a DNA sequence.
        """
        homopolymers = []
        current_base = None
        current_length = 0
        
        for base in seq:
            if base == current_base:
                current_length += 1
            else:
                if current_length >= min_length:
                    homopolymers.append(f"{current_base}x{current_length}")
                current_base = base
                current_length = 1
        
        # Check the last homopolymer
        if current_length >= min_length:
            homopolymers.append(f"{current_base}x{current_length}")
        
        return homopolymers
    
    def _check_rare_codons(self, seq):
        """
        Check for rare codons in a DNA sequence.
        """
        # E. coli rare codons
        rare_codons_list = ["CTA", "ATA", "CGA", "CGG", "AGG", "AGA", "CCC", "TCG"]
        
        rare_codons_found = []
        
        # Check all reading frames
        for frame in range(3):
            # Get the sequence in this reading frame
            frame_seq = seq[frame:]
            
            # Adjust length to be divisible by 3
            frame_seq = frame_seq[:len(frame_seq) - (len(frame_seq) % 3)]
            
            # Check each codon
            for i in range(0, len(frame_seq), 3):
                codon = str(frame_seq[i:i+3])
                if codon in rare_codons_list and codon not in rare_codons_found:
                    rare_codons_found.append(codon)
        
        return rare_codons_found
    
    def _calculate_gc_content(self, seq):
        """
        Calculate the GC content of a DNA sequence.
        """
        gc_count = seq.count("G") + seq.count("C")
        return gc_count / len(seq) if len(seq) > 0 else 0
    
    def _simulate_prediction(self, dna_sequence, embedding=None):
        """
        Simulate a prediction for demonstration purposes.
        """
        # Calculate some features from the sequence
        seq = dna_sequence.upper()
        length = len(seq)
        gc_content = self._calculate_gc_content(seq)
        
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
