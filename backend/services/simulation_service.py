from typing import Dict, Any
import time
import random
import numpy as np
from models.dna_design import DNADesign, PartType

class SimulationService:
    def __init__(self):
        self.cache = {}  # Simple in-memory cache
        self.cache_expiry = 3600  # Cache expiry in seconds (1 hour)
    
    def run_simulation(self, design: DNADesign) -> Dict[str, Any]:
        """
        Run a simulation for a DNA design.
        """
        # Check cache
        cache_key = f"simulation_{design.id}_{design.updated_at.isoformat() if design.updated_at else ''}"
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if time.time() - cache_entry["timestamp"] < self.cache_expiry:
                return cache_entry["data"]
        
        # Analyze the design
        has_promoter = any(part.type == PartType.PROMOTER for part in design.parts)
        has_rbs = any(part.type == PartType.RBS for part in design.parts)
        has_gene = any(part.type == PartType.GENE for part in design.parts)
        has_terminator = any(part.type == PartType.TERMINATOR for part in design.parts)
        
        # Calculate base scores
        growth_rate = 0.5  # Default growth rate
        protein_expression = 0.0  # Default protein expression
        metabolic_burden = 0.3  # Default metabolic burden
        stability = 0.7  # Default stability
        
        # Adjust scores based on design components
        if has_promoter:
            growth_rate += 0.1
            protein_expression += 0.3
        
        if has_rbs:
            protein_expression += 0.2
        
        if has_gene:
            metabolic_burden += 0.2
            protein_expression += 0.3
        
        if has_terminator:
            stability += 0.2
        
        # Check the order of components
        correct_order = True
        promoter_index = -1
        rbs_index = -1
        gene_index = -1
        terminator_index = -1
        
        for i, part in enumerate(design.parts):
            if part.type == PartType.PROMOTER:
                promoter_index = i
            elif part.type == PartType.RBS:
                rbs_index = i
            elif part.type == PartType.GENE:
                gene_index = i
            elif part.type == PartType.TERMINATOR:
                terminator_index = i
        
        # Check if the order is correct: promoter -> RBS -> gene -> terminator
        if promoter_index != -1 and rbs_index != -1 and gene_index != -1 and terminator_index != -1:
            if not (promoter_index < rbs_index < gene_index < terminator_index):
                correct_order = False
                stability -= 0.2
                protein_expression -= 0.2
        
        # Generate time series data
        time_points = 20
        time_series = {
            "time": list(range(time_points)),
            "growth": self._generate_growth_curve(time_points, growth_rate),
            "protein": self._generate_protein_curve(time_points, protein_expression, has_promoter and has_rbs and has_gene),
            "metabolite": self._generate_metabolite_curve(time_points, metabolic_burden, has_gene)
        }
        
        # Add some noise to make it look more realistic
        growth_rate = min(1.0, max(0.0, growth_rate + random.uniform(-0.05, 0.05)))
        protein_expression = min(1.0, max(0.0, protein_expression + random.uniform(-0.05, 0.05)))
        metabolic_burden = min(1.0, max(0.0, metabolic_burden + random.uniform(-0.05, 0.05)))
        stability = min(1.0, max(0.0, stability + random.uniform(-0.05, 0.05)))
        
        # Prepare the result
        result = {
            "growth_rate": growth_rate,
            "protein_expression": protein_expression,
            "metabolic_burden": metabolic_burden,
            "stability": stability,
            "time_series": time_series,
            "notes": []
        }
        
        # Add notes based on the design
        if not has_promoter:
            result["notes"].append("No promoter found. Gene expression may be limited.")
        
        if not has_rbs:
            result["notes"].append("No ribosome binding site found. Protein translation may be inefficient.")
        
        if not has_gene:
            result["notes"].append("No coding sequence found. No protein will be produced.")
        
        if not has_terminator:
            result["notes"].append("No terminator found. Transcription may continue past the intended region.")
        
        if not correct_order:
            result["notes"].append("Components are not in the optimal order. Consider rearranging for better performance.")
        
        # Cache the result
        self.cache[cache_key] = {
            "data": result,
            "timestamp": time.time()
        }
        
        return result
    
    def _generate_growth_curve(self, time_points, growth_rate):
        """
        Generate a simulated growth curve.
        """
        # Logistic growth curve
        K = 1.0  # Carrying capacity
        r = growth_rate * 0.5  # Growth rate parameter
        t = np.linspace(0, time_points - 1, time_points)
        N0 = 0.1  # Initial population
        
        N = K / (1 + ((K - N0) / N0) * np.exp(-r * t))
        
        # Add some noise
        noise = np.random.normal(0, 0.02, time_points)
        N = np.clip(N + noise, 0, 1)
        
        return N.tolist()
    
    def _generate_protein_curve(self, time_points, expression_level, has_expression_system):
        """
        Generate a simulated protein expression curve.
        """
        if not has_expression_system:
            return [0] * time_points
        
        # Protein expression typically follows a sigmoidal curve
        t = np.linspace(0, time_points - 1, time_points)
        k = expression_level * 0.5  # Rate parameter
        midpoint = time_points * 0.3  # When expression reaches half-maximum
        
        protein = expression_level / (1 + np.exp(-k * (t - midpoint)))
        
        # Add some noise
        noise = np.random.normal(0, 0.02, time_points)
        protein = np.clip(protein + noise, 0, 1)
        
        return protein.tolist()
    
    def _generate_metabolite_curve(self, time_points, metabolic_burden, has_gene):
        """
        Generate a simulated metabolite production curve.
        """
        if not has_gene:
            return [0] * time_points
        
        # Metabolite production typically increases over time
        t = np.linspace(0, time_points - 1, time_points)
        k = metabolic_burden * 0.4  # Rate parameter
        
        metabolite = metabolic_burden * (1 - np.exp(-k * t / time_points))
        
        # Add some noise
        noise = np.random.normal(0, 0.02, time_points)
        metabolite = np.clip(metabolite + noise, 0, 1)
        
        return metabolite.tolist()
