from typing import Dict, Any
import time
import re
from models.dna_design import DNADesign, PartType

class SafetyService:
    def __init__(self):
        self.cache = {}  # Simple in-memory cache
        self.cache_expiry = 3600  # Cache expiry in seconds (1 hour)
        
        # Load dangerous sequence patterns
        # In a real implementation, these would be loaded from a database or file
        self.dangerous_patterns = [
            # Toxin genes
            "ATGCCGGTGATGCGGTGCG",  # Example pattern for a toxin gene
            "ATGGCGCAACTGCAACGCG",  # Example pattern for another toxin gene
            
            # Antibiotic resistance genes
            "ATGGCGACCGAACGCGCGG",  # Example pattern for an antibiotic resistance gene
            
            # Virulence factors
            "ATGCGCGTGCAACTGCGCG",  # Example pattern for a virulence factor
        ]
    
    def check_safety(self, design: DNADesign) -> Dict[str, Any]:
        """
        Check the safety of a DNA design.
        """
        # Check cache
        cache_key = f"safety_{design.id}_{design.updated_at.isoformat() if design.updated_at else ''}"
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if time.time() - cache_entry["timestamp"] < self.cache_expiry:
                return cache_entry["data"]
        
        # Get the full sequence
        full_sequence = design.full_sequence
        
        # Initialize safety scores
        overall_score = 0.9  # Start with a high score and deduct based on issues
        toxicity_score = 0.05  # Start with a low toxicity score
        environmental_risk_score = 0.1  # Start with a low environmental risk score
        biocontainment_score = 0.9  # Start with a high biocontainment score
        
        # Check for dangerous sequences
        dangerous_matches = []
        for pattern in self.dangerous_patterns:
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
        
        # Generate recommendations
        recommendations = []
        
        if not has_kill_switch:
            recommendations.append("Consider adding a kill switch for improved biocontainment")
        
        if has_antibiotic_resistance:
            recommendations.append("Antibiotic resistance genes pose environmental risks. Consider alternative selection markers")
        
        if has_toxin:
            recommendations.append("Toxin genes detected. Ensure proper containment and regulatory compliance")
        
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
            "recommendations": recommendations
        }
        
        # Cache the result
        self.cache[cache_key] = {
            "data": result,
            "timestamp": time.time()
        }
        
        return result
