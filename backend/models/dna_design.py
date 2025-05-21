from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class PartType(str, Enum):
    PROMOTER = "promoter"
    GENE = "gene"
    TERMINATOR = "terminator"
    RBS = "rbs"
    OPERATOR = "operator"
    OTHER = "other"

class DNAPart(BaseModel):
    id: str
    name: str
    type: PartType
    sequence: str
    description: Optional[str] = None
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class DNASequence(BaseModel):
    sequence: str
    name: Optional[str] = None
    description: Optional[str] = None

class DNADesign(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    parts: List[DNAPart]
    user_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    simulation_results: Optional[Dict[str, Any]] = None
    safety_score: Optional[Dict[str, Any]] = None
    blockchain_token_id: Optional[str] = None
    
    @property
    def full_sequence(self) -> str:
        """
        Get the full DNA sequence by concatenating all parts.
        """
        return "".join([part.sequence for part in self.parts])
    
    @property
    def length(self) -> int:
        """
        Get the total length of the DNA sequence.
        """
        return sum([len(part.sequence) for part in self.parts])
