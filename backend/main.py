from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import firebase_admin
from firebase_admin import credentials, auth
import os
import json
from datetime import datetime, timedelta

# Import our modules
from models.dna_design import DNADesign, DNASequence, DNAPart
from services.genbank_service import GenBankService
from services.igem_service import IGEMService
from services.ai_service import AIService
from services.blockchain_service import BlockchainService
from services.simulation_service import SimulationService
from services.safety_service import SafetyService

# Initialize Firebase Admin SDK
cred = credentials.Certificate(os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH"))
firebase_admin.initialize_app(cred)

# Initialize FastAPI app
app = FastAPI(
    title="BioForge API",
    description="API for the BioForge synthetic biology platform",
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

# Initialize services
genbank_service = GenBankService()
igem_service = IGEMService()
ai_service = AIService()
blockchain_service = BlockchainService()
simulation_service = SimulationService()
safety_service = SafetyService()

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Authentication dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token["uid"]
        return {"uid": uid}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Token endpoint for authentication
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # In a real implementation, you would verify the credentials with Firebase Auth
    # This is a simplified example
    try:
        user = auth.get_user_by_email(form_data.username)
        # In a real implementation, you would verify the password
        # For now, we'll just return a token
        custom_token = auth.create_custom_token(user.uid)
        return {"access_token": custom_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

# DNA Parts endpoints
@app.get("/api/parts", response_model=List[DNAPart])
async def get_dna_parts(category: Optional[str] = None, query: Optional[str] = None):
    """
    Get DNA parts from the registry.
    Optionally filter by category or search query.
    """
    parts = []
    
    # Get parts from GenBank
    genbank_parts = genbank_service.get_parts(category, query)
    parts.extend(genbank_parts)
    
    # Get parts from iGEM Registry
    igem_parts  query)
    parts.extend(genbank_parts)
    
    # Get parts from iGEM Registry
    igem_parts = igem_service.get_parts(category, query)
    parts.extend(igem_parts)
    
    return parts

# DNA Design endpoints
@app.post("/api/designs", response_model=DNADesign)
async def create_design(design: DNADesign, current_user = Depends(get_current_user)):
    """
    Create a new DNA design.
    """
    # Set the user ID and creation timestamp
    design.user_id = current_user["uid"]
    design.created_at = datetime.now()
    design.updated_at = datetime.now()
    
    # Save the design to the database
    # In a real implementation, you would save to a database
    # For now, we'll just return the design with an ID
    design.id = "design_" + str(int(datetime.now().timestamp()))
    
    return design

@app.get("/api/designs", response_model=List[DNADesign])
async def get_designs(current_user = Depends(get_current_user)):
    """
    Get all designs for the current user.
    """
    # In a real implementation, you would fetch from a database
    # For now, we'll just return an empty list
    return []

@app.get("/api/designs/{design_id}", response_model=DNADesign)
async def get_design(design_id: str, current_user = Depends(get_current_user)):
    """
    Get a specific design by ID.
    """
    # In a real implementation, you would fetch from a database
    # For now, we'll just return a 404
    raise HTTPException(status_code=404, detail="Design not found")

@app.put("/api/designs/{design_id}", response_model=DNADesign)
async def update_design(design_id: str, design: DNADesign, current_user = Depends(get_current_user)):
    """
    Update a specific design by ID.
    """
    # In a real implementation, you would update in a database
    # For now, we'll just return the updated design
    design.id = design_id
    design.user_id = current_user["uid"]
    design.updated_at = datetime.now()
    
    return design

@app.delete("/api/designs/{design_id}", status_code=204)
async def delete_design(design_id: str, current_user = Depends(get_current_user)):
    """
    Delete a specific design by ID.
    """
    # In a real implementation, you would delete from a database
    # For now, we'll just return a 204
    return None

# AI Service endpoints
@app.post("/api/ai/validate", response_model=Dict[str, Any])
async def validate_sequence(sequence: DNASequence):
    """
    Validate a DNA sequence using the AI service.
    """
    validation_result = ai_service.validate_sequence(sequence.sequence)
    return validation_result

@app.post("/api/ai/predict", response_model=Dict[str, Any])
async def predict_function(sequence: DNASequence):
    """
    Predict the function of a DNA sequence using the AI service.
    """
    prediction_result = ai_service.predict_function(sequence.sequence)
    return prediction_result

# Simulation endpoints
@app.post("/api/simulate", response_model=Dict[str, Any])
async def run_simulation(design: DNADesign):
    """
    Run a simulation for a DNA design.
    """
    simulation_result = simulation_service.run_simulation(design)
    return simulation_result

# Safety endpoints
@app.post("/api/safety/check", response_model=Dict[str, Any])
async def check_safety(design: DNADesign):
    """
    Check the safety of a DNA design.
    """
    safety_result = safety_service.check_safety(design)
    return safety_result

# Blockchain endpoints
@app.post("/api/blockchain/mint", response_model=Dict[str, Any])
async def mint_token(design: DNADesign, current_user = Depends(get_current_user)):
    """
    Mint an IP-NFT for a DNA design.
    """
    token_result = blockchain_service.mint_token(design, current_user["uid"])
    return token_result

@app.get("/api/blockchain/tokens", response_model=List[Dict[str, Any]])
async def get_tokens(current_user = Depends(get_current_user)):
    """
    Get all tokens owned by the current user.
    """
    tokens = blockchain_service.get_tokens(current_user["uid"])
    return tokens

# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
