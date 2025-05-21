from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import requests
import xml.etree.ElementTree as ET
import time
import logging
from Bio import Entrez, SeqIO
import io
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set email for Entrez
Entrez.email = os.environ.get("ENTREZ_EMAIL", "bioforge@example.com")

# Initialize FastAPI app
app = FastAPI(
    title="BioForge Data Pipeline Service",
    description="Data pipeline service for the BioForge synthetic biology platform",
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

# Define models
class DNAPart(BaseModel):
    id: str
    name: str
    type: str
    sequence: str
    description: Optional[str] = None
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

# Simple in-memory cache
cache = {}
cache_expiry = 3600  # Cache expiry in seconds (1 hour)

# API endpoints
@app.get("/")
async def root():
    """Root endpoint to check if the service is running."""
    return {"message": "BioForge Data Pipeline Service is running"}

@app.get("/api/parts/search", response_model=List[DNAPart])
async def search_parts(
    query: str = Query(None, description="Search query"),
    category: str = Query(None, description="Part category (promoter, gene, terminator, rbs, operator)"),
    source: str = Query(None, description="Data source (genbank, igem, all)"),
    limit: int = Query(20, description="Maximum number of results to return")
):
    """
    Search for DNA parts across multiple data sources.
    """
    logger.info(f"Searching for parts with query: {query}, category: {category}, source: {source}")
    
    # Build cache key
    cache_key = f"search_{query}_{category}_{source}_{limit}"
    
    # Check cache
    if cache_key in cache:
        cache_entry = cache[cache_key]
        if time.time() - cache_entry["timestamp"] < cache_expiry:
            logger.info(f"Returning cached results for {cache_key}")
            return cache_entry["data"]
    
    results = []
    
    # Search GenBank
    if source is None or source.lower() == "all" or source.lower() == "genbank":
        genbank_results = await search_genbank(query, category, limit)
        results.extend(genbank_results)
    
    # Search iGEM Registry
    if source is None or source.lower() == "all" or source.lower() == "igem":
        igem_results = await search_igem(query, category, limit)
        results.extend(igem_results)
    
    # Limit results
    if len(results) > limit:
        results = results[:limit]
    
    # Cache results
    cache[cache_key] = {
        "data": results,
        "timestamp": time.time()
    }
    
    return results

@app.get("/api/parts/{part_id}", response_model=DNAPart)
async def get_part(part_id: str):
    """
    Get a specific DNA part by ID.
    """
    logger.info(f"Getting part with ID: {part_id}")
    
    # Build cache key
    cache_key = f"part_{part_id}"
    
    # Check cache
    if cache_key in cache:
        cache_entry = cache[cache_key]
        if time.time() - cache_entry["timestamp"] < cache_expiry:
            logger.info(f"Returning cached result for {cache_key}")
            return cache_entry["data"]
    
    # Determine the source from the ID prefix
    if part_id.startswith("genbank_"):
        # Get from GenBank
        genbank_id = part_id[8:]  # Remove "genbank_" prefix
        part = await get_genbank_part(genbank_id)
    elif part_id.startswith("igem_"):
        # Get from iGEM Registry
        igem_id = part_id[5:]  # Remove "igem_" prefix
        part = await get_igem_part(igem_id)
    else:
        raise HTTPException(status_code=404, detail=f"Part not found with ID: {part_id}")
    
    if part is None:
        raise HTTPException(status_code=404, detail=f"Part not found with ID: {part_id}")
    
    # Cache result
    cache[cache_key] = {
        "data": part,
        "timestamp": time.time()
    }
    
    return part

@app.get("/api/sources")
async def get_sources():
    """
    Get available data sources.
    """
    return {
        "sources": [
            {
                "id": "genbank",
                "name": "GenBank",
                "description": "NCBI GenBank database",
                "url": "https://www.ncbi.nlm.nih.gov/genbank/"
            },
            {
                "id": "igem",
                "name": "iGEM Registry",
                "description": "Registry of Standard Biological Parts",
                "url": "http://parts.igem.org/"
            }
        ]
    }

@app.get("/api/categories")
async def get_categories():
    """
    Get available part categories.
    """
    return {
        "categories": [
            {
                "id": "promoter",
                "name": "Promoter",
                "description": "DNA sequence that initiates transcription of a gene"
            },
            {
                "id": "gene",
                "name": "Gene",
                "description": "DNA sequence that codes for a protein or RNA molecule"
            },
            {
                "id": "terminator",
                "name": "Terminator",
                "description": "DNA sequence that signals the end of transcription"
            },
            {
                "id": "rbs",
                "name": "Ribosome Binding Site",
                "description": "DNA sequence that facilitates ribosome binding for translation"
            },
            {
                "id": "operator",
                "name": "Operator",
                "description": "DNA sequence that regulates gene expression"
            },
            {
                "id": "other",
                "name": "Other",
                "description": "Other DNA parts"
            }
        ]
    }

async def search_genbank(query: Optional[str], category: Optional[str], limit: int) -> List[DNAPart]:
    """
    Search GenBank for DNA parts.
    """
    # Build the search query
    search_query = ""
    
    if category:
        if category.lower() == "promoter":
            search_query += "promoter[Title] OR regulatory[Title]"
        elif category.lower() == "gene":
            search_query += "gene[Title] OR coding[Title]"
        elif category.lower() == "terminator":
            search_query += "terminator[Title]"
        elif category.lower() == "rbs":
            search_query += "ribosome binding site[Title] OR RBS[Title]"
        elif category.lower() == "operator":
            search_query += "operator[Title]"
    
    if query:
        if search_query:
            search_query += f" AND {query}"
        else:
            search_query = query
    
    if not search_query:
        search_query = "synthetic[Title] AND biology[Title]"
    
    # Check cache
    cache_key = f"genbank_{search_query}_{limit}"
    if cache_key in cache:
        cache_entry = cache[cache_key]
        if time.time() - cache_entry["timestamp"] < cache_expiry:
            return cache_entry["data"]
    
    # Search GenBank
    try:
        # Use Entrez to search GenBank
        handle = Entrez.esearch(db="nucleotide", term=search_query, retmax=limit)
        record = Entrez.read(handle)
        handle.close()
        
        id_list = record["IdList"]
        
        if not id_list:
            return []
        
        # Fetch the sequences
        handle = Entrez.efetch(db="nucleotide", id=id_list, rettype="gb", retmode="text")
        records = list(SeqIO.parse(handle, "genbank"))
        handle.close()
        
        # Convert to DNAPart objects
        parts = []
        for record in records:
            part_type = _determine_genbank_part_type(record)
            
            part = DNAPart(
                id=f"genbank_{record.id}",
                name=record.description[:50],  # Truncate long descriptions
                type=part_type,
                sequence=str(record.seq),
                description=record.description,
                source="GenBank",
                metadata={
                    "accession": record.id,
                    "organism": record.annotations.get("organism", "Unknown"),
                    "taxonomy": record.annotations.get("taxonomy", []),
                    "references": [ref.title for ref in record.annotations.get("references", [])]
                }
            )
            parts.append(part)
        
        # Cache the results
        cache[cache_key] = {
            "data": parts,
            "timestamp": time.time()
        }
        
        return parts
    
    except Exception as e:
        logger.error(f"Error fetching from GenBank: {e}")
        return []

async def get_genbank_part(genbank_id: str) -> Optional[DNAPart]:
    """
    Get a specific part from GenBank.
    """
    try:
        # Fetch the sequence
        handle = Entrez.efetch(db="nucleotide", id=genbank_id, rettype="gb", retmode="text")
        records = list(SeqIO.parse(handle, "genbank"))
        handle.close()
        
        if not records:
            return None
        
        record = records[0]
        part_type = _determine_genbank_part_type(record)
        
        part = DNAPart(
            id=f"genbank_{record.id}",
            name=record.description[:50],  # Truncate long descriptions
            type=part_type,
            sequence=str(record.seq),
            description=record.description,
            source="GenBank",
            metadata={
                "accession": record.id,
                "organism": record.annotations.get("organism", "Unknown"),
                "taxonomy": record.annotations.get("taxonomy", []),
                "references": [ref.title for ref in record.annotations.get("references", [])]
            }
        )
        
        return part
    
    except Exception as e:
        logger.error(f"Error fetching from GenBank: {e}")
        return None

async def search_igem(query: Optional[str], category: Optional[str], limit: int) -> List[DNAPart]:
    """
    Search iGEM Registry for DNA parts.
    """
    # In a real implementation, this would call the iGEM Registry API
    # For now, we'll return some sample parts
    
    # Build search parameters
    search_params = {}
    
    if category:
        if category.lower() == "promoter":
            search_params["type"] = "Promoter"
        elif category.lower() == "gene":
            search_params["type"] = "Coding"
        elif category.lower() == "terminator":
            search_params["type"] = "Terminator"
        elif category.lower() == "rbs":
            search_params["type"] = "RBS"
        elif category.lower() == "operator":
            search_params["type"] = "Regulatory"
    
    if query:
        search_params["name"] = query
    
    # Check cache
    cache_key = f"igem_{json.dumps(search_params)}_{limit}"
    if cache_key in cache:
        cache_entry = cache[cache_key]
        if time.time() - cache_entry["timestamp"] < cache_expiry:
            return cache_entry["data"]
    
    # Get sample parts
    sample_parts = _get_igem_sample_parts(category)
    
    # Filter by query if provided
    if query:
        sample_parts = [
            part for part in sample_parts
            if query.lower() in part.name.lower() or (part.description and query.lower() in part.description.lower())
        ]
    
    # Limit results
    if len(sample_parts) > limit:
        sample_parts = sample_parts[:limit]
    
    # Cache the results
    cache[cache_key] = {
        "data": sample_parts,
        "timestamp": time.time()
    }
    
    return sample_parts

async def get_igem_part(igem_id: str) -> Optional[DNAPart]:
    """
    Get a specific part from iGEM Registry.
    """
    # In a real implementation, this would call the iGEM Registry API
    # For now, we'll return a sample part if it matches one of our samples
    
    sample_parts = _get_igem_sample_parts(None)
    
    for part in sample_parts:
        if part.id == f"igem_{igem_id}":
            return part
    
    return None

def _determine_genbank_part_type(record) -> str:
    """
    Determine the part type based on the GenBank record.
    """
    description = record.description.lower()
    features = [feature.type.lower() for feature in record.features]
    
    if "promoter" in description or "promoter" in features:
        return "promoter"
    elif "terminator" in description or "terminator" in features:
        return "terminator"
    elif "rbs" in description or "ribosome binding site" in features:
        return "rbs"
    elif "operator" in description or "operator" in features:
        return "operator"
    elif "gene" in description or "cds" in features or "coding" in features:
        return "gene"
    else:
        return "other"

def _get_igem_sample_parts(category: Optional[str]) -> List[DNAPart]:
    """
    Get sample parts from iGEM Registry.
    """
    sample_parts = [
        DNAPart(
            id="igem_BBa_R0010",
            name="LacI promoter",
            type="promoter",
            sequence="CAATACGCAAACCGCCTCTCCCCGCGCGTTGGCCGATTCATTAATGCAGCTGGCACGACAGGTTTCCCGACTGGAAAGCGGGCAGTGAGCGCAACGCAATTAATGTGAGTTAGCTCACTCATTAGGCACCCCAGGCTTTACACTTTATGCTTCCGGCTCGTATGTTGTGTGGAATTGTGAGCGGATAACAATTTCACACA",
            description="LacI repressible promoter",
            source="iGEM Registry",
            metadata={
                "igem_id": "BBa_R0010",
                "igem_type": "Promoter",
                "url": "http://parts.igem.org/Part:BBa_R0010"
            }
        ),
        DNAPart(
            id="igem_BBa_B0034",
            name="RBS",
            type="rbs",
            sequence="AAAGAGGAGAAA",
            description="RBS based on Elowitz repressilator",
            source="iGEM Registry",
            metadata={
                "igem_id": "BBa_B0034",
                "igem_type": "RBS",
                "url": "http://parts.igem.org/Part:BBa_B0034"
            }
        ),
        DNAPart(
            id="igem_BBa_E0040",
            name="GFP",
            type="gene",
            sequence="ATGCGTAAAGGAGAAGAACTTTTCACTGGAGTTGTCCCAATTCTTGTTGAATTAGATGGTGATGTTAATGGGCACAAATTTTCTGTCAGTGGAGAGGGTGAAGGTGATGCAACATACGGAAAACTTACCCTTAAATTTATTTGCACTACTGGAAAACTACCTGTTCCATGGCCAACACTTGTCACTACTTTCGGTTATGGTGTTCAATGCTTTGCGAGATACCCAGATCATATGAAACAGCATGACTTTTTCAAGAGTGCCATGCCCGAAGGTTATGTACAGGAAAGAACTATATTTTTCAAAGATGACGGGAACTACAAGACACGTGCTGAAGTCAAGTTTGAAGGTGATACCCTTGTTAATAGAATCGAGTTAAAAGGTATTGATTTTAAAGAAGATGGAAACATTCTTGGACACAAATTGGAATACAACTATAACTCACACAATGTATACATCATGGCAGACAAACAAAAGAATGGAATCAAAGTTAACTTCAAAATTAGACACAACATTGAAGATGGAAGCGTTCAACTAGCAGACCATTATCAACAAAATACTCCAATTGGCGATGGCCCTGTCCTTTTACCAGACAACCATTACCTGTCCACACAATCTGCCCTTTCGAAAGATCCCAACGAAAAGAGAGACCACATGGTCCTTCTTGAGTTTGTAACAGCTGCTGGGATTACACATGGCATGGATGAACTATACAAATAATAA",
            description="GFP generator",
            source="iGEM Registry",
            metadata={
                "igem_id": "BBa_E0040",
                "igem_type": "Coding",
                "url": "http://parts.igem.org/Part:BBa_E0040"
            }
        ),
        DNAPart(
            id="igem_BBa_B0015",
            name="Terminator",
            type="terminator",
            sequence="CCAGGCATCAAATAAAACGAAAGGCTCAGTCGAAAGACTGGGCCTTTCGTTTTATCTGTTGTTTGTCGGTGAACGCTCTCTACTAGAGTCACACTGGCTCACCTTCGGGTGGGCCTTTCTGCGTTTATA",
            description="Double terminator",
            source="iGEM Registry",
            metadata={
                "igem_id": "BBa_B0015",
                "igem_type": "Terminator",
                "url": "http://parts.igem.org/Part:BBa_B0015"
            }
        ),
        DNAPart(
            id="igem_BBa_C0062",
            name="LuxR",
            type="gene",
            sequence="ATGAAAAACATAAATGCCGACGACACATACAGAATAATTAATAAAATTAAAGCTTGTAGAAGCAATAATGATATTAATCAATGCTTATCTGATATGACTAAAATGGTACATTGTGAATATTATTTACTCGCGATCATTTATCCTCATTCTATGGTTAAATCTGATATTTCAATCCTAGATAATTACCCTAAAAAATGGAGGCAATATTATGATGACGCTAATTTAATAAAATATGATCCTATAGTAGATTATTCTAACTCCAATCATTCACCAATTAATTGGAATATATTTGAAAACAATGCTGTAAATAAAAAATCTCCAAATGTAATTAAAGAAGCGAAAACATCAGGTCTTATCACTGGGTTTAGTTTCCCTATTCATACGGCTAACAATGGCTTCGGAATGCTTAGTTTTGCACATTCAGAAAAAGACAACTATATAGATAGTTTATTTTTACATGCGTGTATGAACATACCATTAATTGTTCCTTCTCTAGTTGATAATTATCGAAAAATAAATATAGCAAATAATAAATCAAACAACGATTTAACCAAAAGAGAAAAAGAATGTTTAGCGTGGGCATGCGAAGGAAAAAGCTCTTGGGATATTTCAAAAATATTAGGTTGCAGTGAGCGTACTGTCACTTTCCATTTAACCAATGCGCAAATGAAACTCAATACAACAAACCGCTGCCAAAGTATTTCTAAAGCAATTTTAACAGGAGCAATTGATTGCCCATACTTTAAAAATTAATAACACTGATAGTGCTAGTGTAGATCAC",
            description="LuxR repressor/activator",
            source="iGEM Registry",
            metadata={
                "igem_id": "BBa_C0062",
                "igem_type": "Coding",
                "url": "http://parts.igem.org/Part:BBa_C0062"
            }
        ),
        DNAPart(
            id="igem_BBa_R0062",
            name="LuxR responsive promoter",
            type="promoter",
            sequence="ACCTGTAGGATCGTACAGGTTTACGCAAGAAAATGGTTTGTTATAGTCGAATAAA",
            description="LuxR responsive promoter",
            source="iGEM Registry",
            metadata={
                "igem_id": "BBa_R0062",
                "igem_type": "Promoter",
                "url": "http://parts.igem.org/Part:BBa_R0062"
            }
        )
    ]
    
    if category:
        return [part for part in sample_parts if part.type == category.lower()]
    
    return sample_parts

# Main entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
