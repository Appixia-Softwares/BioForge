from typing import List, Optional
from models.dna_design import DNAPart, PartType
import requests
import xml.etree.ElementTree as ET
import time
import os
from Bio import Entrez, SeqIO

# Set email for Entrez
Entrez.email = os.environ.get("ENTREZ_EMAIL", "bioforge@example.com")

class GenBankService:
    def __init__(self):
        self.base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.cache = {}  # Simple in-memory cache
        self.cache_expiry = 3600  # Cache expiry in seconds (1 hour)
    
    def get_parts(self, category: Optional[str] = None, query: Optional[str] = None) -> List[DNAPart]:
        """
        Get DNA parts from GenBank.
        Optionally filter by category or search query.
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
        cache_key = f"genbank_{search_query}"
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if time.time() - cache_entry["timestamp"] < self.cache_expiry:
                return cache_entry["data"]
        
        # Search GenBank
        try:
            # Use Entrez to search GenBank
            handle = Entrez.esearch(db="nucleotide", term=search_query, retmax=20)
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
                part_type = self._determine_part_type(record)
                
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
            self.cache[cache_key] = {
                "data": parts,
                "timestamp": time.time()
            }
            
            return parts
        
        except Exception as e:
            print(f"Error fetching from GenBank: {e}")
            return []
    
    def _determine_part_type(self, record) -> PartType:
        """
        Determine the part type based on the GenBank record.
        """
        description = record.description.lower()
        features = [feature.type.lower() for feature in record.features]
        
        if "promoter" in description or "promoter" in features:
            return PartType.PROMOTER
        elif "terminator" in description or "terminator" in features:
            return PartType.TERMINATOR
        elif "rbs" in description or "ribosome binding site" in features:
            return PartType.RBS
        elif "operator" in description or "operator" in features:
            return PartType.OPERATOR
        elif "gene" in description or "cds" in features or "coding" in features:
            return PartType.GENE
        else:
            return PartType.OTHER
