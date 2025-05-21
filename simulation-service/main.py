from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import numpy as np
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="BioForge Simulation Service",
    description="Simulation service for the BioForge synthetic biology platform",
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

class SimulationParameters(BaseModel):
    time_points: int = 20
    environment: str = "standard"  # standard, nutrient-rich, minimal, stress
    host_organism: str = "ecoli"  # ecoli, yeast, mammalian, plant
    temperature: float = 37.0  # in Celsius
    custom_parameters: Optional[Dict[str, Any]] = None

# API endpoints
@app.get("/")
async def root():
    """Root endpoint to check if the service is running."""
    return {"message": "BioForge Simulation Service is running"}

@app.post("/api/simulate")
async def run_simulation(design: DNADesign, parameters: Optional[SimulationParameters] = None):
    """Run a simulation for a DNA design."""
    logger.info(f"Running simulation for design: {design.name}")
    
    # Use default parameters if none provided
    if parameters is None:
        parameters = SimulationParameters()
    
    # Analyze the design
    has_promoter = any(part.type.lower() == "promoter" for part in design.parts)
    has_rbs = any(part.type.lower() == "rbs" for part in design.parts)
    has_gene = any(part.type.lower() == "gene" for part in design.parts)
    has_terminator = any(part.type.lower() == "terminator" for part in design.parts)
    
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
    
    # Adjust based on environment
    if parameters.environment == "nutrient-rich":
        growth_rate += 0.1
        protein_expression += 0.1
    elif parameters.environment == "minimal":
        growth_rate -= 0.1
        protein_expression -= 0.1
    elif parameters.environment == "stress":
        growth_rate -= 0.2
        stability -= 0.1
    
    # Adjust based on host organism
    if parameters.host_organism == "yeast":
        growth_rate -= 0.05
        protein_expression -= 0.1
    elif parameters.host_organism == "mammalian":
        growth_rate -= 0.2
        protein_expression -= 0.2
    elif parameters.host_organism == "plant":
        growth_rate -= 0.3
        protein_expression -= 0.3
    
    # Adjust based on temperature
    if parameters.temperature < 30.0 or parameters.temperature > 40.0:
        growth_rate -= 0.1
        stability -= 0.1
    
    # Check the order of components
    correct_order = True
    promoter_index = -1
    rbs_index = -1
    gene_index = -1
    terminator_index = -1
    
    for i, part in enumerate(design.parts):
        if part.type.lower() == "promoter":
            promoter_index = i
        elif part.type.lower() == "rbs":
            rbs_index = i
        elif part.type.lower() == "gene":
            gene_index = i
        elif part.type.lower() == "terminator":
            terminator_index = i
    
    # Check if the order is correct: promoter -> RBS -> gene -> terminator
    if promoter_index != -1 and rbs_index != -1 and gene_index != -1 and terminator_index != -1:
        if not (promoter_index < rbs_index < gene_index < terminator_index):
            correct_order = False
            stability -= 0.2
            protein_expression -= 0.2
    
    # Generate time series data
    time_points = parameters.time_points
    time_series = {
        "time": list(range(time_points)),
        "growth": _generate_growth_curve(time_points, growth_rate),
        "protein": _generate_protein_curve(time_points, protein_expression, has_promoter and has_rbs and has_gene),
        "metabolite": _generate_metabolite_curve(time_points, metabolic_burden, has_gene)
    }
    
    # Add some noise to make it look more realistic
    growth_rate = min(1.0, max(0.0, growth_rate + np.random.uniform(-0.05, 0.05)))
    protein_expression = min(1.0, max(0.0, protein_expression + np.random.uniform(-0.05, 0.05)))
    metabolic_burden = min(1.0, max(0.0, metabolic_burden + np.random.uniform(-0.05, 0.05)))
    stability = min(1.0, max(0.0, stability + np.random.uniform(-0.05, 0.05)))
    
    # Prepare the result
    result = {
        "growth_rate": growth_rate,
        "protein_expression": protein_expression,
        "metabolic_burden": metabolic_burden,
        "stability": stability,
        "time_series": time_series,
        "parameters": {
            "time_points": parameters.time_points,
            "environment": parameters.environment,
            "host_organism": parameters.host_organism,
            "temperature": parameters.temperature
        },
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
    
    return result

@app.post("/api/simulate/protein-folding")
async def simulate_protein_folding(sequence: str):
    """Simulate protein folding for a given amino acid sequence."""
    logger.info(f"Simulating protein folding for sequence of length: {len(sequence)}")
    
    # In a real implementation, this would use a protein folding simulation
    # For now, we'll just return some simulated data
    
    # Calculate some basic properties
    hydrophobic_residues = sum(1 for aa in sequence if aa in "AVILMFYW")
    hydrophobic_ratio = hydrophobic_residues / len(sequence) if len(sequence) > 0 else 0
    
    charged_residues = sum(1 for aa in sequence if aa in "DEKRH")
    charged_ratio = charged_residues / len(sequence) if len(sequence) > 0 else 0
    
    # Simulate secondary structure propensities
    helix_propensity = 0.0
    sheet_propensity = 0.0
    
    for aa in sequence:
        if aa in "AVILMF":
            helix_propensity += 0.1
        elif aa in "TVIY":
            sheet_propensity += 0.1
    
    helix_propensity = min(1.0, helix_propensity / len(sequence) * 3) if len(sequence) > 0 else 0
    sheet_propensity = min(1.0, sheet_propensity / len(sequence) * 3) if len(sequence) > 0 else 0
    coil_propensity = 1.0 - helix_propensity - sheet_propensity
    
    # Simulate folding energy
    folding_energy = -50.0 - hydrophobic_ratio * 100.0 + np.random.normal(0, 10)
    
    # Simulate folding time
    folding_time = 1.0 + len(sequence) / 100.0 + np.random.exponential(1.0)
    
    # Simulate stability
    stability = 0.7 + hydrophobic_ratio * 0.3 - charged_ratio * 0.2 + np.random.normal(0, 0.1)
    stability = min(1.0, max(0.0, stability))
    
    return {
        "sequence_length": len(sequence),
        "hydrophobic_ratio": hydrophobic_ratio,
        "charged_ratio": charged_ratio,
        "secondary_structure": {
            "helix": helix_propensity,
            "sheet": sheet_propensity,
            "coil": coil_propensity
        },
        "folding_energy": folding_energy,
        "folding_time": folding_time,
        "stability": stability,
        "aggregation_propensity": 0.3 + charged_ratio * 0.2 + np.random.normal(0, 0.1)
    }

@app.post("/api/simulate/metabolic-pathway")
async def simulate_metabolic_pathway(designs: List[DNADesign], parameters: Optional[SimulationParameters] = None):
    """Simulate a metabolic pathway with multiple designs."""
    logger.info(f"Simulating metabolic pathway with {len(designs)} designs")
    
    # Use default parameters if none provided
    if parameters is None:
        parameters = SimulationParameters()
    
    # In a real implementation, this would use a metabolic pathway simulation
    # For now, we'll just return some simulated data
    
    # Simulate each design
    design_results = []
    for design in designs:
        result = await run_simulation(design, parameters)
        design_results.append({
            "design_id": design.id,
            "design_name": design.name,
            "growth_rate": result["growth_rate"],
            "protein_expression": result["protein_expression"],
            "metabolic_burden": result["metabolic_burden"]
        })
    
    # Calculate pathway efficiency
    if len(designs) > 0:
        avg_protein_expression = sum(r["protein_expression"] for r in design_results) / len(design_results)
        avg_metabolic_burden = sum(r["metabolic_burden"] for r in design_results) / len(design_results)
        pathway_efficiency = avg_protein_expression * (1.0 - avg_metabolic_burden)
    else:
        pathway_efficiency = 0.0
    
    # Generate pathway time series
    time_points = parameters.time_points
    pathway_time_series = {
        "time": list(range(time_points)),
        "substrate": _generate_substrate_curve(time_points, pathway_efficiency),
        "intermediate": _generate_intermediate_curve(time_points, pathway_efficiency, len(designs)),
        "product": _generate_product_curve(time_points, pathway_efficiency)
    }
    
    return {
        "pathway_efficiency": pathway_efficiency,
        "design_results": design_results,
        "time_series": pathway_time_series,
        "bottleneck_index": np.argmin([r["protein_expression"] for r in design_results]) if design_results else -1,
        "yield": pathway_efficiency * 0.8 + np.random.normal(0, 0.05),
        "productivity": pathway_efficiency * 0.7 + np.random.normal(0, 0.05)
    }

def _generate_growth_curve(time_points, growth_rate):
    """Generate a simulated growth curve."""
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

def _generate_protein_curve(time_points, expression_level, has_expression_system):
    """Generate a simulated protein expression curve."""
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

def _generate_metabolite_curve(time_points, metabolic_burden, has_gene):
    """Generate a simulated metabolite production curve."""
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

def _generate_substrate_curve(time_points, pathway_efficiency):
    """Generate a simulated substrate consumption curve."""
    # Substrate typically decreases over time
    t = np.linspace(0, time_points - 1, time_points)
    k = pathway_efficiency * 0.5  # Rate parameter
    
    substrate = 1.0 * np.exp(-k * t / time_points)
    
    # Add some noise
    noise = np.random.normal(0, 0.02, time_points)
    substrate = np.clip(substrate + noise, 0, 1)
    
    return substrate.tolist()

def _generate_intermediate_curve(time_points, pathway_efficiency, num_steps):
    """Generate a simulated intermediate metabolite curve."""
    if num_steps <= 1:
        return [0] * time_points
    
    # Intermediate typically rises and then falls
    t = np.linspace(0, time_points - 1, time_points)
    k1 = pathway_efficiency * 0.6  # Production rate
    k2 = pathway_efficiency * 0.4  # Consumption rate
    
    intermediate = 0.5 * (1 - np.exp(-k1 * t / time_points)) * np.exp(-k2 * t / time_points)
    
    # Add some noise
    noise = np.random.normal(0, 0.02, time_points)
    intermediate = np.clip(intermediate + noise, 0, 1)
    
    return intermediate.tolist()

def _generate_product_curve(time_points, pathway_efficiency):
    """Generate a simulated product formation curve."""
    # Product typically increases over time
    t = np.linspace(0, time_points - 1, time_points)
    k = pathway_efficiency * 0.3  # Rate parameter
    
    product = pathway_efficiency * (1 - np.exp(-k * t / time_points))
    
    # Add some noise
    noise = np.random.normal(0, 0.02, time_points)
    product = np.clip(product + noise, 0, 1)
    
    return product.tolist()

# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
