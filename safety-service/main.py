from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import re
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="BioForge Safety Service",
    description="Safety and biocontainment service for the BioForge synthetic biology platform",
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
class DNAPart(BaseModel):
    id: str
    name: str
    type: str
    sequence: str
    description: Optional[str] = None
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class DNADesign(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    parts: List[DNAPart]
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

# Load dangerous sequence patterns
# In a real implementation, these would be loaded from a database or file
DANGEROUS_PATTERNS = [
    # Toxin genes
    "ATGCCGGTGATGCGGTGCG",  # Example pattern for a toxin gene
    "ATGGCGCAACTGCAACGCG",  # Example pattern for another toxin gene
    
    # Antibiotic resistance genes
    "ATGGCGACCGAACGCGCGG",  # Example pattern for an antibiotic resistance gene
    
    # Virulence factors
    "ATGCGCGTGCAACTGCGCG",  # Example pattern for a virulence factor
]

# Load restricted organisms
RESTRICTED_ORGANISMS = [
    "Bacillus anthracis",
    "Yersinia pestis",
    "Francisella tularensis",
    "Variola virus",
    "Ebola virus",
    "Marburg virus",
]

# API endpoints
@app.get("/")
async def root():
    """Root endpoint to check if the service is running."""
    return {"message": "BioForge Safety Service is running"}

@app.post("/api/safety/check")
async def check_safety(design: DNADesign):
    """Check the safety of a DNA design."""
    logger.info(f"Checking safety for design: {design.name}")
    
    # Get the full sequence
    full_sequence = "".join([part.sequence for part in design.parts])
    
    # Initialize safety scores
    overall_score = 0.9  # Start with a high score and deduct based on issues
    toxicity_score = 0.05  # Start with a low toxicity score
    environmental_risk_score = 0.1  # Start with a low environmental risk score
    biocontainment_score = 0.9  # Start with a high biocontainment score
    
    # Check for dangerous sequences
    dangerous_matches = []
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, full_sequence, re.IGNORECASE):
            dangerous_matches.append(pattern)
    
    if dangerous_matches:
        overall_score -= 0.3
        toxicity_score += 0.3
        environmental_risk_score += 0.2
    
    # Check for antibiotic resistance genes
    has_antibiotic_resistance = any(
        part.name.lower().find("antibiotic") != -1 or 
        part.name.lower().find("resistance") != -1 
        for part in design.parts
    )
    
    if has_antibiotic_resistance:
        overall_score -= 0.2
        environmental_risk_score += 0.3
        biocontainment_score -= 0.2
    
    # Check for biocontainment features
    has_kill_switch = any(
        part.name.lower().find("kill") != -1 or 
        part.name.lower().find("suicide") != -1 
        for part in design.parts
    )
    
    if not has_kill_switch:
        biocontainment_score -= 0.3
    
    # Check for toxin genes
    has_toxin = any(
        part.name.lower().find("toxin") != -1 or 
        part.name.lower().find("poison") != -1 
        for part in design.parts
    )
    
    if has_toxin:
        overall_score -= 0.3
        toxicity_score += 0.4
        environmental_risk_score += 0.3
    
    # Check for restricted organisms
    restricted_organism_matches = []
    for organism in RESTRICTED_ORGANISMS:
        if (design.description and organism.lower() in design.description.lower()) or any(
            organism.lower() in part.description.lower() if part.description else False
            for part in design.parts
        ):
            restricted_organism_matches.append(organism)
    
    if restricted_organism_matches:
        overall_score -= 0.5
        toxicity_score += 0.5
        environmental_risk_score += 0.5
        biocontainment_score -= 0.5
    
    # Generate recommendations
    recommendations = []
    
    if not has_kill_switch:
        recommendations.append("Consider adding a kill switch for improved biocontainment")
    
    if has_antibiotic_resistance:
        recommendations.append("Antibiotic resistance genes pose environmental risks. Consider alternative selection markers")
    
    if has_toxin:
        recommendations.append("Toxin genes detected. Ensure proper containment and regulatory compliance")
    
    if restricted_organism_matches:
        recommendations.append(f"Design contains references to restricted organisms: {', '.join(restricted_organism_matches)}. This may be subject to regulatory restrictions")
    
    if overall_score < 0.6:
        recommendations.append("This design has significant safety concerns. Review and revise before proceeding")
    
    # Ensure scores are within bounds
    overall_score = max(0.0, min(1.0, overall_score))
    toxicity_score = max(0.0, min(1.0, toxicity_score))
    environmental_risk_score = max(0.0, min(1.0, environmental_risk_score))
    biocontainment_score = max(0.0, min(1.0, biocontainment_score))
    
    # Prepare the result
    result = {
        "overall": overall_score,
        "toxicity": toxicity_score,
        "environmental_risk": environmental_risk_score,
        "biocontainment": biocontainment_score,
        "dangerous_sequences": len(dangerous_matches),
        "restricted_organisms": restricted_organism_matches,
        "recommendations": recommendations,
        "regulatory_flags": {
            "dual_use_research_of_concern": overall_score < 0.5,
            "select_agent": len(restricted_organism_matches) > 0,
            "needs_review": overall_score < 0.7
        }
    }
    
    return result

@app.post("/api/safety/analyze-sequence")
async def analyze_sequence(sequence: str):
    """Analyze a DNA sequence for safety concerns."""
    logger.info(f"Analyzing sequence of length: {len(sequence)}")
    
    # Check for dangerous sequences
    dangerous_matches = []
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, sequence, re.IGNORECASE):
            dangerous_matches.append(pattern)
    
    # Calculate GC content
    gc_count = sequence.upper().count("G") + sequence.upper().count("C")
    gc_content = gc_count / len(sequence) if len(sequence) > 0 else 0
    
    # Check for homopolymers (runs of the same nucleotide)
    homopolymers = []
    for base in "ATGC":
        pattern = base * 6  # Look for runs of 6 or more
        if pattern in sequence.upper():
            homopolymers.append(f"{base}x6+")
    
    # Prepare the result
    result = {
        "sequence_length": len(sequence),
        "gc_content": gc_content,
        "dangerous_patterns": len(dangerous_matches) > 0,
        "homopolymers": homopolymers,
        "safety_concerns": len(dangerous_matches) > 0,
        "recommendations": []
    }
    
    if len(dangerous_matches) > 0:
        result["recommendations"].append("Sequence contains patterns associated with dangerous genes")
    
    if homopolymers:
        result["recommendations"].append("Sequence contains homopolymer regions which may affect stability")
    
    if gc_content < 0.3:
        result["recommendations"].append("Low GC content may affect stability")
    elif gc_content > 0.7:
        result["recommendations"].append("High GC content may affect ease of handling")
    
    return result

# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
