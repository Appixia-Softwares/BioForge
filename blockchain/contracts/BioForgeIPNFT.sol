// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

/**
 * @title BioForgeIPNFT
 * @dev ERC721 token for BioForge IP-NFTs with royalty distribution
 */
contract BioForgeIPNFT is ERC721, ERC721URIStorage, ERC721Enumerable, Ownable {
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;
    
    // Mapping from token ID to design hash
    mapping(uint256 => string) private _designHashes;
    
    // Mapping from token ID to contributors
    mapping(uint256 => address[]) private _contributors;
    
    // Mapping from token ID to contributor shares (in basis points, 1/100 of a percent)
    mapping(uint256 => uint256[]) private _contributorShares;
    
    // Mapping from design hash to token ID
    mapping(string => uint256) private _designTokens;
    
    // Events
    event TokenMinted(uint256 indexed tokenId, string designHash, address[] contributors, uint256[] shares);
    event RoyaltyPaid(uint256 indexed tokenId, address indexed recipient, uint256 amount);

    constructor() ERC721("BioForgeIPNFT", "BFIP") {}

    /**
     * @dev Mints a new IP-NFT
     * @param to The address that will own the minted token
     * @param tokenURI The token URI for metadata
     * @param designHash The hash of the design data
     * @param contributors Array of contributor addresses
     * @param shares Array of contributor shares (in basis points, must sum to 10000)
     * @return The ID of the newly minted token
     */
    function mintToken(
        address to,
        string memory tokenURI,
        string memory designHash,
        address[] memory contributors,
        uint256[] memory shares
    ) public returns (uint256) {
        require(bytes(designHash).length > 0, "Design hash cannot be empty");
        require(contributors.length > 0, "Must have at least one contributor");
        require(contributors.length == shares.length, "Contributors and shares arrays must have the same length");
        
        // Check if design already has a token
        require(_designTokens[designHash] == 0, "Design already has a token");
        
        // Validate shares
        uint256 totalShares = 0;
        for (uint256 i = 0; i < shares.length; i++) {
            totalShares += shares[i];
        }
        require(totalShares == 10000, "Shares must sum to 10000 (100%)");
        
        // Mint the token
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, tokenURI);
        
        // Store design hash and contributors
        _designHashes[tokenId] = designHash;
        _contributors[tokenId] = contributors;
        _contributorShares[tokenId] = shares;
        _designTokens[designHash] = tokenId;
        
        emit TokenMinted(tokenId, designHash, contributors, shares);
        
        return tokenId;
    }
    
    /**
     * @dev Distributes royalties to contributors
     * @param tokenId The ID of the token to distribute royalties for
     */
    function distributeRoyalties(uint256 tokenId) public payable {
        require(_exists(tokenId), "Token does not exist");
        require(msg.value > 0, "Must send ETH to distribute");
        
        address[] memory contributors = _contributors[tokenId];
        uint256[] memory shares = _contributorShares[tokenId];
        
        uint256 remaining = msg.value;
        
        for (uint256 i = 0; i < contributors.length; i++) {
            uint256 amount = (msg.value * shares[i]) / 10000;
            remaining -= amount;
            
            (bool success, ) = contributors[i].call{value: amount}("");
            require(success, "Failed to send royalty");
            
            emit RoyaltyPaid(tokenId, contributors[i], amount);
        }
        
        // Send any dust (from rounding) to the first contributor
        if (remaining > 0) {
            (bool success, ) = contributors[0].call{value: remaining}("");
            require(success, "Failed to send remaining royalty");
        }
    }
    
    /**
     * @dev Gets the design hash for a token
     * @param tokenId The ID of the token
     * @return The design hash
     */
    function getDesignHash(uint256 tokenId) public view returns (string memory) {
        require(_exists(tokenId), "Token does not exist");
        return _designHashes[tokenId];
    }
    
    /**
     * @dev Gets the contributors for a token
     * @param tokenId The ID of the token
     * @return Array of contributor addresses
     */
    function getContributors(uint256 tokenId) public view returns (address[] memory) {
        require(_exists(tokenId), "Token does not exist");
        return _contributors[tokenId];
    }
    
    /**
     * @dev Gets the contributor shares for a token
     * @param tokenId The ID of the token
     * @return Array of contributor shares (in basis points)
     */
    function getContributorShares(uint256 tokenId) public view returns (uint256[] memory) {
        require(_exists(tokenId), "Token does not exist");
        return _contributorShares[tokenId];
    }
    
    /**
     * @dev Gets the token ID for a design hash
     * @param designHash The design hash
     * @return The token ID, or 0 if no token exists for the design
     */
    function getTokenIdForDesign(string memory designHash) public view returns (uint256) {
        return _designTokens[designHash];
    }
    
    /**
     * @dev Gets all tokens owned by an address
     * @param owner The address to query
     * @return Array of token IDs
     */
    function tokensOfOwner(address owner) public view returns (uint256[] memory) {
        uint256 tokenCount = balanceOf(owner);
        uint256[] memory tokenIds = new uint256[](tokenCount);
        
        for (uint256 i = 0; i < tokenCount; i++) {
            tokenIds[i] = tokenOfOwnerByIndex(owner, i);
        }
        
        return tokenIds;
    }
    
    // Override functions required by Solidity
    
    function _beforeTokenTransfer(address from, address to, uint256 tokenId, uint256 batchSize)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}
