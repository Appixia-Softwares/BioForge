from typing import List, Optional
from models.dna_design import DNAPart, PartType
import requests
import xml.etree.ElementTree as ET
import time
import os

class IGEMService:
    def __init__(self):
        self.base_url = "http://parts.igem.org/partsdb/api/"
        self.cache = {}  # Simple in-memory cache
        self.cache_expiry = 3600  # Cache expiry in seconds (1 hour)
    
    def get_parts(self, category: Optional[str] = None, query: Optional[str] = None) -> List[DNAPart]:
        """
        Get DNA parts from the iGEM Registry.
        Optionally filter by category or search query.
        """
        # Build the search query
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
        cache_key = f"igem_{str(search_params)}"
        if cache_key in self.cache:
            cache_entry = self.cache[cache_key]
            if time.time() - cache_entry["timestamp"] < self.cache_expiry:
                return cache_entry["data"]
        
        # Search iGEM Registry
        try:
            # Note: This is a simplified example. The actual iGEM API might be different.
            # You would need to check the iGEM Registry API documentation for the correct endpoints.
            response = requests.get(f"{self.base_url}/search", params=search_params)
            response.raise_for_status()
            
            # Parse the XML response
            # This is a simplified example. The actual response format might be different.
            root = ET.fromstring(response.text)
            
            parts = []
            for part_elem in root.findall(".//part"):
                part_id = part_elem.get("id")
                part_name = part_elem.find("name").text
                part_type_str = part_elem.find("type").text
                part_sequence = part_elem.find("sequence").text
                part_description = part_elem.find("description").text
                
                # Map iGEM part type to our PartType enum
                part_type = self._map_igem_type(part_type_str)
                
                part = DNAPart(
                    id=f"igem_{part_id}",
                    name=part_name,
                    type=part_type,
                    sequence=part_sequence,
                    description=part_description,
                    source="iGEM Registry",
                    metadata={
                        "igem_id": part_id,
                        "igem_type": part_type_str,
                        "url": f"http://parts.igem.org/Part:{part_id}"
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
            print(f"Error fetching from iGEM Registry: {e}")
            # For demonstration purposes, return some sample parts
            return self._get_sample_parts(category)
    
    def _map_igem_type(self, igem_type: str) -> PartType:
        """
        Map iGEM part type to our PartType enum.
        """
        igem_type = igem_type.lower()
        
        if "promoter" in igem_type:
            return PartType.PROMOTER
        elif "terminator" in igem_type:
            return PartType.TERMINATOR
        elif "rbs" in igem_type or "ribosome binding site" in igem_type:
            return PartType.RBS
        elif "regulatory" in igem_type or "operator" in igem_type:
            return PartType.OPERATOR
        elif "coding" in igem_type or "gene" in igem_type:
            return PartType.GENE
        else:
            return PartType.OTHER
    
    def _get_sample_parts(self, category: Optional[str] = None) -> List[DNAPart]:
        """
        Get sample parts for demonstration purposes.
        """
        sample_parts = [
            DNAPart(
                id="igem_BBa_R0010",
                name="LacI promoter",
                type=PartType.PROMOTER,
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
                type=PartType.RBS,
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
                type=PartType.GENE,
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
                type=PartType.TERMINATOR,
                sequence="CCAGGCATCAAATAAAACGAAAGGCTCAGTCGAAAGACTGGGCCTTTCGTTTTATCTGTTGTTTGTCGGTGAACGCTCTCTACTAGAGTCACACTGGCTCACCTTCGGGTGGGCCTTTCTGCGTTTATA",
                description="Double terminator",
                source="iGEM Registry",
                metadata={
                    "igem_id": "BBa_B0015",
                    "igem_type": "Terminator",
                    "url": "http://parts.igem.org/Part:BBa_B0015"
                }
            )
        ]
        
        if category:
            category_type = None
            if category.lower() == "promoter":
                category_type = PartType.PROMOTER
            elif category.lower() == "gene":
                category_type = PartType.GENE
            elif category.lower() == "terminator":
                category_type = PartType.TERMINATOR
            elif category.lower() == "rbs":
                category_type = PartType.RBS
            elif category.lower() == "operator":
                category_type = PartType.OPERATOR
            
            if category_type:
                return [part for part in sample_parts if part.type == category_type]
        
        return sample_parts
