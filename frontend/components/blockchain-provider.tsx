"use client"

import type React from "react"
import { createContext, useContext, useEffect, useState } from "react"
import { ethers } from "ethers"
import { useToast } from "@/components/ui/use-toast"

// ABI for the BioForgeIPNFT contract
const BioForgeIPNFTABI = [
  "function mintToken(address to, string memory tokenURI, string memory designHash, address[] memory contributors, uint256[] memory shares) public returns (uint256)",
  "function tokensOfOwner(address owner) public view returns (uint256[] memory)",
  "function tokenURI(uint256 tokenId) public view returns (string memory)",
  "function getDesignHash(uint256 tokenId) public view returns (string memory)",
  "function getContributors(uint256 tokenId) public view returns (address[] memory)",
  "function getContributorShares(uint256 tokenId) public view returns (uint256[] memory)",
]

// Contract address (this would be set after deployment)
const CONTRACT_ADDRESS = process.env.NEXT_PUBLIC_CONTRACT_ADDRESS || "0x0000000000000000000000000000000000000000"

type BlockchainContextType = {
  connected: boolean
  connecting: boolean
  account: string | null
  chainId: number | null
  provider: ethers.providers.Web3Provider | null
  signer: ethers.Signer | null
  contract: ethers.Contract | null
  connect: () => Promise<void>
  disconnect: () => void
  mintToken: (
    tokenURI: string,
    designHash: string,
    contributors: string[],
    shares: number[],
  ) => Promise<{ tokenId: string; txHash: string }>
  getTokensOfOwner: (owner: string) => Promise<string[]>
}

const BlockchainContext = createContext<BlockchainContextType>({
  connected: false,
  connecting: false,
  account: null,
  chainId: null,
  provider: null,
  signer: null,
  contract: null,
  connect: async () => {},
  disconnect: () => {},
  mintToken: async () => ({ tokenId: "", txHash: "" }),
  getTokensOfOwner: async () => [],
})

export function BlockchainProvider({ children }: { children: React.ReactNode }) {
  const [connected, setConnected] = useState(false)
  const [connecting, setConnecting] = useState(false)
  const [account, setAccount] = useState<string | null>(null)
  const [chainId, setChainId] = useState<number | null>(null)
  const [provider, setProvider] = useState<ethers.providers.Web3Provider | null>(null)
  const [signer, setSigner] = useState<ethers.Signer | null>(null)
  const [contract, setContract] = useState<ethers.Contract | null>(null)
  const { toast } = useToast()

  // Initialize provider and contract
  useEffect(() => {
    if (typeof window !== "undefined" && window.ethereum) {
      // Create a Web3Provider from the Ethereum provider
      const web3Provider = new ethers.providers.Web3Provider(window.ethereum)
      setProvider(web3Provider)

      // Create contract instance
      const contractInstance = new ethers.Contract(CONTRACT_ADDRESS, BioForgeIPNFTABI, web3Provider)
      setContract(contractInstance)

      // Check if already connected
      web3Provider
        .listAccounts()
        .then((accounts) => {
          if (accounts.length > 0) {
            setAccount(accounts[0])
            setConnected(true)
            return web3Provider.getSigner()
          }
          return null
        })
        .then((signer) => {
          if (signer) {
            setSigner(signer)
            setContract(contractInstance.connect(signer))
          }
        })
        .catch((error) => {
          console.error("Error checking connection:", error)
        })

      // Get the network
      web3Provider
        .getNetwork()
        .then((network) => {
          setChainId(network.chainId)
        })
        .catch((error) => {
          console.error("Error getting network:", error)
        })

      // Listen for account changes
      window.ethereum.on("accountsChanged", (accounts: string[]) => {
        if (accounts.length === 0) {
          // User disconnected
          setConnected(false)
          setAccount(null)
          setSigner(null)
        } else {
          // User switched accounts
          setAccount(accounts[0])
          const newSigner = web3Provider.getSigner()
          setSigner(newSigner)
          setContract(contractInstance.connect(newSigner))
        }
      })

      // Listen for chain changes
      window.ethereum.on("chainChanged", (chainId: string) => {
        window.location.reload()
      })

      return () => {
        // Clean up listeners
        window.ethereum.removeAllListeners("accountsChanged")
        window.ethereum.removeAllListeners("chainChanged")
      }
    }
  }, [])

  // Connect to MetaMask
  const connect = async () => {
    if (!provider) {
      toast({
        title: "MetaMask not found",
        description: "Please install MetaMask to use blockchain features",
        variant: "destructive",
      })
      return
    }

    setConnecting(true)

    try {
      // Request account access
      const accounts = await window.ethereum.request({ method: "eth_requestAccounts" })
      setAccount(accounts[0])
      setConnected(true)

      // Get the signer
      const signer = provider.getSigner()
      setSigner(signer)

      // Connect the contract to the signer
      if (contract) {
        setContract(contract.connect(signer))
      }

      toast({
        title: "Connected to MetaMask",
        description: `Connected to account ${accounts[0].substring(0, 6)}...${accounts[0].substring(38)}`,
      })
    } catch (error) {
      console.error("Error connecting to MetaMask:", error)
      toast({
        title: "Connection failed",
        description: "Failed to connect to MetaMask",
        variant: "destructive",
      })
    } finally {
      setConnecting(false)
    }
  }

  // Disconnect from MetaMask
  const disconnect = () => {
    setConnected(false)
    setAccount(null)
    setSigner(null)
    toast({
      title: "Disconnected",
      description: "Disconnected from MetaMask",
    })
  }

  // Mint a new IP-NFT token
  const mintToken = async (
    tokenURI: string,
    designHash: string,
    contributors: string[],
    shares: number[],
  ): Promise<{ tokenId: string; txHash: string }> => {
    if (!contract || !signer || !account) {
      throw new Error("Not connected to blockchain")
    }

    // Convert shares to basis points (1/100 of a percent)
    const basisPointShares = shares.map((share) => Math.round(share * 100))

    // Ensure shares sum to 10000 (100%)
    const totalShares = basisPointShares.reduce((a, b) => a + b, 0)
    if (totalShares !== 10000) {
      throw new Error(`Shares must sum to 100%, got ${totalShares / 100}%`)
    }

    try {
      // Call the mintToken function
      const tx = await contract.mintToken(account, tokenURI, designHash, contributors, basisPointShares)
      const receipt = await tx.wait()

      // Get the token ID from the event logs
      const event = receipt.events?.find((e: any) => e.event === "TokenMinted")
      const tokenId = event?.args?.tokenId.toString() || "0"

      return {
        tokenId,
        txHash: tx.hash,
      }
    } catch (error) {
      console.error("Error minting token:", error)
      throw error
    }
  }

  // Get all tokens owned by an address
  const getTokensOfOwner = async (owner: string): Promise<string[]> => {
    if (!contract) {
      throw new Error("Contract not initialized")
    }

    try {
      const tokens = await contract.tokensOfOwner(owner)
      return tokens.map((token: ethers.BigNumber) => token.toString())
    } catch (error) {
      console.error("Error getting tokens:", error)
      throw error
    }
  }

  return (
    <BlockchainContext.Provider
      value={{
        connected,
        connecting,
        account,
        chainId,
        provider,
        signer,
        contract,
        connect,
        disconnect,
        mintToken,
        getTokensOfOwner,
      }}
    >
      {children}
    </BlockchainContext.Provider>
  )
}

export const useBlockchain = () => useContext(BlockchainContext)
