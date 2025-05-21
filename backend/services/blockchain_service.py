from typing import Dict, Any, List
import json
import time
import os
import hashlib
from web3 import Web3
from eth_account import Account
from eth_account.signers.local import LocalAccount
from models.dna_design import DNADesign

# Load environment variables
POLYGON_RPC_URL = os.environ.get("POLYGON_RPC_URL", "https://polygon-rpc.com")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY", "")  # This should be securely stored
CONTRACT_ADDRESS = os.environ.get("CONTRACT_ADDRESS", "")

# IP-NFT Smart Contract ABI (simplified)
CONTRACT_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "tokenURI", "type": "string"},
            {"internalType": "string", "name": "designHash", "type": "string"},
            {"internalType": "address[]", "name": "contributors", "type": "address[]"},
            {"internalType": "uint256[]", "name": "shares", "type": "uint256[]"}
        ],
        "name": "mintToken",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "owner", "type": "address"}],
        "name": "tokensOfOwner",
        "outputs": [{"internalType": "uint256[]", "name": "", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "tokenURI",
        "outputs": [{"internalType": "string", "name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]

class BlockchainService:
    def __init__(self):
        self.w3 = None
        self.account = None
        self.contract = None
        self.initialized = False
        self.simulation_mode = True
        
        # Try to initialize Web3
        try:
            self.w3 = Web3(Web3.HTTPProvider(POLYGON_RPC_URL))
            
            if PRIVATE_KEY:
                self.account = Account.from_key(PRIVATE_KEY)
                print(f"Blockchain account initialized: {self.account.address}")
            
            if CONTRACT_ADDRESS:
                self.contract = self.w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=CONTRACT_ABI)
                print(f"Smart contract initialized at {CONTRACT_ADDRESS}")
            
            if self.w3.is_connected() and self.account and self.contract:
                self.initialized = True
                self.simulation_mode = False
                print("Blockchain service initialized successfully")
            else:
                print("Blockchain service initialized in simulation mode")
        except Exception as e:
            print(f"Error initializing blockchain service: {e}")
            print("Blockchain service will run in simulation mode")
    
    def mint_token(self, design: DNADesign, user_id: str) -> Dict[str, Any]:
        """
        Mint an IP-NFT for a DNA design.
        """
        if self.simulation_mode:
            return self._simulate_mint_token(design, user_id)
        
        try:
            # Create a hash of the design
            design_json = json.dumps(design.dict(), sort_keys=True)
            design_hash = hashlib.sha256(design_json.encode()).hexdigest()
            
            # Create token metadata
            token_metadata = {
                "name": f"BioForge: {design.name}",
                "description": design.description or "A synthetic biology design created with BioForge",
                "image": "https://bioforge.example.com/nft-image.png",  # Placeholder
                "external_url": f"https://bioforge.example.com/designs/{design.id}",
                "attributes": [
                    {"trait_type": "Creator", "value": user_id},
                    {"trait_type": "Parts", "value": len(design.parts)},
                    {"trait_type": "Length", "value": design.length},
                    {"trait_type": "Created", "value": design.created_at.isoformat() if design.created_at else ""}
                ]
            }
            
            # In a real implementation, you would upload this metadata to IPFS
            # For now, we'll just use a placeholder URI
            token_uri = f"https://bioforge.example.com/metadata/{design_hash}"
            
            # Set up the transaction
            contributors = [self.account.address]  # In a real implementation, this would include all contributors
            shares = [100]  # 100% to the creator
            
            # Build the transaction
            tx = self.contract.functions.mintToken(
                token_uri,
                design_hash,
                contributors,
                shares
            ).build_transaction({
                'from': self.account.address,
                'nonce': self.w3.eth.get_transaction_count(self.account.address),
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })
            
            # Sign the transaction
            signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=self.account.key)
            
            # Send the transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for the transaction to be mined
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Get the token ID from the event logs
            token_id = None
            for log in tx_receipt.logs:
                # In a real implementation, you would parse the event logs to get the token ID
                # For now, we'll just use a placeholder
                token_id = int(time.time())
            
            return {
                "success": True,
                "token_id": token_id,
                "transaction_hash": tx_hash.hex(),
                "block_number": tx_receipt.blockNumber,
                "token_uri": token_uri,
                "design_hash": design_hash
            }
        
        except Exception as e:
            print(f"Error minting token: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_tokens(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all tokens owned by a user.
        """
        if self.simulation_mode:
            return self._simulate_get_tokens(user_id)
        
        try:
            # Convert user_id to an Ethereum address
            # In a real implementation, you would have a mapping from user_id to address
            address = self.account.address
            
            # Call the contract to get the tokens
            token_ids = self.contract.functions.tokensOfOwner(address).call()
            
            tokens = []
            for token_id in token_ids:
                # Get the token URI
                token_uri = self.contract.functions.tokenURI(token_id).call()
                
                # In a real implementation, you would fetch the metadata from the URI
                # For now, we'll just use placeholder data
                tokens.append({
                    "token_id": token_id,
                    "token_uri": token_uri,
                    "name": f"BioForge Design #{token_id}",
                    "description": "A synthetic biology design created with BioForge",
                    "image": "https://bioforge.example.com/nft-image.png"  # Placeholder
                })
            
            return tokens
        
        except Exception as e:
            print(f"Error getting tokens: {e}")
            return []
    
    def _simulate_mint_token(self, design: DNADesign, user_id: str) -> Dict[str, Any]:
        """
        Simulate minting a token for demonstration purposes.
        """
        # Create a hash of the design
        design_json = json.dumps({
            "id": design.id,
            "name": design.name,
            "parts": [part.id for part in design.parts]
        }, sort_keys=True)
        design_hash = hashlib.sha256(design_json.encode()).hexdigest()
        
        # Simulate a token ID
        token_id = int(time.time())
        
        return {
            "success": True,
            "token_id": token_id,
            "transaction_hash": f"0x{design_hash[:64]}",
            "block_number": int(time.time()),
            "token_uri": f"https://bioforge.example.com/metadata/{design_hash}",
            "design_hash": design_hash,
            "note": "This is a simulated transaction (blockchain service is in simulation mode)"
        }
    
    def _simulate_get_tokens(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Simulate getting tokens for demonstration purposes.
        """
        # Generate some sample tokens
        return [
            {
                "token_id": int(time.time()) - 86400,  # Yesterday
                "token_uri": "https://bioforge.example.com/metadata/sample1",
                "name": "GFP Expression System",
                "description": "A synthetic biology design for expressing Green Fluorescent Protein",
                "image": "https://bioforge.example.com/nft-image.png",
                "note": "This is a simulated token (blockchain service is in simulation mode)"
            },
            {
                "token_id": int(time.time()) - 172800,  # 2 days ago
                "token_uri": "https://bioforge.example.com/metadata/sample2",
                "name": "Plastic Degradation Circuit",
                "description": "A synthetic biology design for degrading PET plastic",
                "image": "https://bioforge.example.com/nft-image.png",
                "note": "This is a simulated token (blockchain service is in simulation mode)"
            }
        ]
