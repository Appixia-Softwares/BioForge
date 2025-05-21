"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ProteinStructureViewer } from "@/components/protein-structure-viewer"
import { useToast } from "@/components/ui/use-toast"
import { Loader2 } from "lucide-react"

export default function ProteinViewerPage() {
  const { toast } = useToast()
  const [proteinSequence, setProteinSequence] = useState("")
  const [proteinName, setProteinName] = useState("")
  const [loading, setLoading] = useState(false)
  const [pdbData, setPdbData] = useState<string | null>(null)
  const [predictionData, setPredictionData] = useState<any>(null)
  const [activeTab, setActiveTab] = useState("structure")

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!proteinSequence.trim()) {
      toast({
        title: "Error",
        description: "Please enter a protein sequence",
        variant: "destructive",
      })
      return
    }

    setLoading(true)

    try {
      // In a real implementation, this would be an API call to the AI service
      // For now, we'll just simulate a response

      // Simulate API call delay
      await new Promise((resolve) => setTimeout(resolve, 3000))

      // Simulate PDB data (this is a minimal PDB format example)
      const simulatedPdbData = `
HEADER    SIMULATED PROTEIN STRUCTURE
TITLE     BIOFORGE PROTEIN VIEWER DEMO
REMARK    THIS IS A SIMULATED STRUCTURE FOR DEMONSTRATION PURPOSES
ATOM      1  N   MET A   1      10.000  10.000  10.000  1.00 20.00           N  
ATOM      2  CA  MET A   1      11.000  10.000  10.000  1.00 20.00           C  
ATOM      3  C   MET A   1      11.500  11.400  10.000  1.00 20.00           C  
ATOM      4  O   MET A   1      10.700  12.300  10.000  1.00 20.00           O  
ATOM      5  CB  MET A   1      11.800   9.000  11.000  1.00 20.00           C  
ATOM      6  N   ALA A   2      12.800  11.600  10.000  1.00 20.00           N  
ATOM      7  CA  ALA A   2      13.400  12.900  10.000  1.00 20.00           C  
ATOM      8  C   ALA A   2      14.900  12.800  10.000  1.00 20.00           C  
ATOM      9  O   ALA A   2      15.500  11.800  10.400  1.00 20.00           O  
ATOM     10  CB  ALA A   2      13.000  13.700  11.200  1.00 20.00           C  
END
      `.trim()

      setPdbData(simulatedPdbData)

      // Simulate prediction data
      setPredictionData({
        residue_count: 2,
        atom_count: 10,
        sequence_length: proteinSequence.length,
        confidence: 0.85,
        secondary_structure: {
          alpha_helix: 0.6,
          beta_sheet: 0.2,
          coil: 0.2,
        },
        domains: [{ name: "Sample Domain", start: 1, end: proteinSequence.length, confidence: 0.9 }],
      })

      setActiveTab("structure")

      toast({
        title: "Structure prediction complete",
        description: "The protein structure has been successfully predicted.",
      })
    } catch (error) {
      console.error("Error predicting structure:", error)
      toast({
        title: "Error",
        description: "Failed to predict protein structure. Please try again.",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container mx-auto py-6 px-4">
      <h1 className="text-2xl font-bold mb-6">Protein Structure Prediction</h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle>Input Protein Sequence</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="protein-name">Protein Name (optional)</Label>
                <Input
                  id="protein-name"
                  value={proteinName}
                  onChange={(e) => setProteinName(e.target.value)}
                  placeholder="e.g., GFP Variant"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="protein-sequence">Protein Sequence (amino acids)</Label>
                <Textarea
                  id="protein-sequence"
                  value={proteinSequence}
                  onChange={(e) => setProteinSequence(e.target.value)}
                  placeholder="Enter amino acid sequence (e.g., MVSKGEELFT...)"
                  rows={10}
                  className="font-mono"
                />
              </div>

              <Button type="submit" className="w-full bg-green-600 hover:bg-green-700" disabled={loading}>
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Predicting...
                  </>
                ) : (
                  "Predict Structure"
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>Protein Structure Visualization</CardTitle>
          </CardHeader>
          <CardContent>
            {pdbData ? (
              <div>
                <Tabs value={activeTab} onValueChange={setActiveTab}>
                  <TabsList className="grid w-full grid-cols-2">
                    <TabsTrigger value="structure">3D Structure</TabsTrigger>
                    <TabsTrigger value="analysis">Analysis</TabsTrigger>
                  </TabsList>

                  <TabsContent value="structure" className="pt-4">
                    <div className="flex justify-center">
                      <ProteinStructureViewer pdbData={pdbData} width={500} height={400} />
                    </div>
                  </TabsContent>

                  <TabsContent value="analysis" className="pt-4">
                    {predictionData && (
                      <div className="space-y-4">
                        <div>
                          <h3 className="text-lg font-medium mb-2">Structure Summary</h3>
                          <div className="grid grid-cols-2 gap-4">
                            <div className="bg-gray-50 p-3 rounded-lg">
                              <p className="text-sm text-gray-500">Residues</p>
                              <p className="text-xl font-semibold">{predictionData.residue_count}</p>
                            </div>
                            <div className="bg-gray-50 p-3 rounded-lg">
                              <p className="text-sm text-gray-500">Atoms</p>
                              <p className="text-xl font-semibold">{predictionData.atom_count}</p>
                            </div>
                            <div className="bg-gray-50 p-3 rounded-lg">
                              <p className="text-sm text-gray-500">Sequence Length</p>
                              <p className="text-xl font-semibold">{predictionData.sequence_length}</p>
                            </div>
                            <div className="bg-gray-50 p-3 rounded-lg">
                              <p className="text-sm text-gray-500">Confidence</p>
                              <p className="text-xl font-semibold">{(predictionData.confidence * 100).toFixed(1)}%</p>
                            </div>
                          </div>
                        </div>

                        <div>
                          <h3 className="text-lg font-medium mb-2">Secondary Structure</h3>
                          <div className="space-y-2">
                            <div>
                              <div className="flex justify-between mb-1">
                                <span className="text-sm">Alpha Helix</span>
                                <span className="text-sm font-medium">
                                  {(predictionData.secondary_structure.alpha_helix * 100).toFixed(1)}%
                                </span>
                              </div>
                              <div className="w-full bg-gray-200 rounded-full h-2">
                                <div
                                  className="bg-blue-500 h-2 rounded-full"
                                  style={{ width: `${predictionData.secondary_structure.alpha_helix * 100}%` }}
                                ></div>
                              </div>
                            </div>

                            <div>
                              <div className="flex justify-between mb-1">
                                <span className="text-sm">Beta Sheet</span>
                                <span className="text-sm font-medium">
                                  {(predictionData.secondary_structure.beta_sheet * 100).toFixed(1)}%
                                </span>
                              </div>
                              <div className="w-full bg-gray-200 rounded-full h-2">
                                <div
                                  className="bg-green-500 h-2 rounded-full"
                                  style={{ width: `${predictionData.secondary_structure.beta_sheet * 100}%` }}
                                ></div>
                              </div>
                            </div>

                            <div>
                              <div className="flex justify-between mb-1">
                                <span className="text-sm">Random Coil</span>
                                <span className="text-sm font-medium">
                                  {(predictionData.secondary_structure.coil * 100).toFixed(1)}%
                                </span>
                              </div>
                              <div className="w-full bg-gray-200 rounded-full h-2">
                                <div
                                  className="bg-purple-500 h-2 rounded-full"
                                  style={{ width: `${predictionData.secondary_structure.coil * 100}%` }}
                                ></div>
                              </div>
                            </div>
                          </div>
                        </div>

                        <div>
                          <h3 className="text-lg font-medium mb-2">Predicted Domains</h3>
                          <div className="space-y-2">
                            {predictionData.domains.map((domain, index) => (
                              <div key={index} className="bg-gray-50 p-3 rounded-lg">
                                <div className="flex justify-between">
                                  <span className="font-medium">{domain.name}</span>
                                  <span className="text-sm text-gray-500">
                                    {domain.start}-{domain.end}
                                  </span>
                                </div>
                                <div className="text-sm text-gray-500">
                                  Confidence: {(domain.confidence * 100).toFixed(1)}%
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>
                      </div>
                    )}
                  </TabsContent>
                </Tabs>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-80 text-gray-400">
                <p>No protein structure to display</p>
                <p className="text-sm mt-2">Enter a protein sequence and click "Predict Structure"</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
