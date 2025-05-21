"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { useBlockchain } from "@/components/blockchain-provider"
import { useToast } from "@/components/ui/use-toast"
import { Loader2, ExternalLink, Copy, Check } from "lucide-react"

export default function BlockchainPage() {
  const { connected, connecting, account, chainId, connect, disconnect } = useBlockchain()
  const { toast } = useToast()
  const [tokens, setTokens] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)

  // Load tokens when connected
  useEffect(() => {
    if (connected && account) {
      loadTokens()
    } else {
      setTokens([])
    }
  }, [connected, account])

  // Load tokens owned by the connected account
  const loadTokens = async () => {
    if (!connected || !account) return

    setLoading(true)
    try {
      // In a real implementation, this would call the blockchain service
      // For now, we'll just use sample data
      setTimeout(() => {
        setTokens([
          {
            id: "1",
            name: "GFP Expression System",
            description: "A synthetic biology design for expressing Green Fluorescent Protein",
            image: "/placeholder.svg?height=200&width=200",
            creator: account,
            createdAt: new Date().toISOString(),
            txHash: "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
          },
          {
            id: "2",
            name: "Plastic Degradation Circuit",
            description: "A synthetic biology design for degrading PET plastic",
            image: "/placeholder.svg?height=200&width=200",
            creator: account,
            createdAt: new Date(Date.now() - 86400000).toISOString(), // Yesterday
            txHash: "0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
          },
        ])
        setLoading(false)
      }, 1000)
    } catch (error) {
      console.error("Error loading tokens:", error)
      toast({
        title: "Error",
        description: "Failed to load tokens",
        variant: "destructive",
      })
      setLoading(false)
    }
  }

  // Copy address to clipboard
  const copyAddress = () => {
    if (account) {
      navigator.clipboard.writeText(account)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
      toast({
        title: "Address copied",
        description: "Wallet address copied to clipboard",
      })
    }
  }

  // Get network name from chain ID
  const getNetworkName = (chainId: number | null) => {
    if (!chainId) return "Unknown"
    switch (chainId) {
      case 1:
        return "Ethereum Mainnet"
      case 137:
        return "Polygon Mainnet"
      case 80001:
        return "Polygon Mumbai Testnet"
      default:
        return `Chain ID: ${chainId}`
    }
  }

  // Format address for display
  const formatAddress = (address: string) => {
    return `${address.substring(0, 6)}...${address.substring(address.length - 4)}`
  }

  return (
    <div className="container mx-auto py-6 px-4">
      <h1 className="text-2xl font-bold mb-6">Blockchain Integration</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Wallet Connection Card */}
        <Card>
          <CardHeader>
            <CardTitle>Wallet Connection</CardTitle>
            <CardDescription>Connect your wallet to interact with the blockchain</CardDescription>
          </CardHeader>
          <CardContent>
            {connected ? (
              <div className="space-y-4">
                <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div>
                    <p className="text-sm text-gray-500">Connected Account</p>
                    <p className="font-mono">{formatAddress(account || "")}</p>
                  </div>
                  <Button variant="ghost" size="icon" onClick={copyAddress}>
                    {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                  </Button>
                </div>
                <div className="p-3 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-500">Network</p>
                  <p>{getNetworkName(chainId)}</p>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-40">
                <p className="text-gray-500 mb-4">Not connected to a wallet</p>
              </div>
            )}
          </CardContent>
          <CardFooter>
            {connected ? (
              <Button variant="outline" className="w-full" onClick={disconnect}>
                Disconnect Wallet
              </Button>
            ) : (
              <Button className="w-full bg-green-600 hover:bg-green-700" onClick={connect} disabled={connecting}>
                {connecting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Connecting...
                  </>
                ) : (
                  "Connect Wallet"
                )}
              </Button>
            )}
          </CardFooter>
        </Card>

        {/* IP-NFT Tokens */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Your IP-NFT Tokens</CardTitle>
            <CardDescription>Intellectual property tokens for your synthetic biology designs</CardDescription>
          </CardHeader>
          <CardContent>
            {!connected ? (
              <div className="flex flex-col items-center justify-center h-60 text-center">
                <p className="text-gray-500 mb-2">Connect your wallet to view your tokens</p>
                <Button className="mt-4 bg-green-600 hover:bg-green-700" onClick={connect} disabled={connecting}>
                  {connecting ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Connecting...
                    </>
                  ) : (
                    "Connect Wallet"
                  )}
                </Button>
              </div>
            ) : loading ? (
              <div className="flex flex-col items-center justify-center h-60">
                <Loader2 className="h-8 w-8 animate-spin text-green-600" />
                <p className="mt-4 text-gray-500">Loading your tokens...</p>
              </div>
            ) : tokens.length === 0 ? (
              <div className="flex flex-col items-center justify-center h-60 text-center">
                <p className="text-gray-500 mb-2">You don't have any IP-NFT tokens yet</p>
                <p className="text-sm text-gray-400">
                  Create a design in the Designer and mint it as an IP-NFT to see it here
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {tokens.map((token) => (
                  <div key={token.id} className="border rounded-lg overflow-hidden">
                    <div className="aspect-square bg-gray-100 flex items-center justify-center">
                      <img
                        src={token.image || "/placeholder.svg"}
                        alt={token.name}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <div className="p-4">
                      <h3 className="font-semibold truncate">{token.name}</h3>
                      <p className="text-sm text-gray-500 line-clamp-2 h-10">{token.description}</p>
                      <div className="mt-2 flex justify-between items-center">
                        <span className="text-xs text-gray-400">Token ID: {token.id}</span>
                        <a
                          href={`https://mumbai.polygonscan.com/tx/${token.txHash}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-xs text-blue-500 flex items-center"
                        >
                          View <ExternalLink className="h-3 w-3 ml-1" />
                        </a>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
          {connected && tokens.length > 0 && (
            <CardFooter>
              <Button variant="outline" className="w-full" onClick={loadTokens} disabled={loading}>
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Refreshing...
                  </>
                ) : (
                  "Refresh Tokens"
                )}
              </Button>
            </CardFooter>
          )}
        </Card>
      </div>
    </div>
  )
}
