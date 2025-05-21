"use client"

import { useState } from "react"
import { DndProvider } from "react-dnd"
import { HTML5Backend } from "react-dnd-html5-backend"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Card, CardContent } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { useToast } from "@/components/ui/use-toast"
import { DnaViewer } from "@/components/dna-viewer"
import { DnaPalette } from "@/components/dna-palette"
import { DnaCanvas } from "@/components/dna-canvas"
import { SimulationPanel } from "@/components/simulation-panel"
import { SafetyPanel } from "@/components/safety-panel"
import { Save, Play, Share, Download } from "lucide-react"

export default function DesignerPage() {
  const { toast } = useToast()
  const [activeTab, setActiveTab] = useState("design")
  const [sequence, setSequence] = useState<any[]>([])
  const [simulationResults, setSimulationResults] = useState(null)
  const [safetyScore, setSafetyScore] = useState(null)

  const handleRunSimulation = async () => {
    if (sequence.length === 0) {
      toast({
        title: "No sequence to simulate",
        description: "Please add DNA parts to your design first.",
        variant: "destructive",
      })
      return
    }

    toast({
      title: "Simulation started",
      description: "Your design is being simulated. This may take a few moments.",
    })

    // This would be an API call to the simulation service
    // For now, we'll just set a timeout to simulate the process
    setTimeout(() => {
      setSimulationResults({
        growth_rate: 0.75,
        protein_expression: 0.82,
        metabolic_burden: 0.35,
        stability: 0.91,
      })
      setActiveTab("simulate")

      toast({
        title: "Simulation complete",
        description: "Your design has been successfully simulated.",
      })
    }, 3000)
  }

  const handleSafetyCheck = async () => {
    if (sequence.length === 0) {
      toast({
        title: "No sequence to check",
        description: "Please add DNA parts to your design first.",
        variant: "destructive",
      })
      return
    }

    toast({
      title: "Safety check started",
      description: "Your design is being analyzed for safety concerns.",
    })

    // This would be an API call to the safety service
    setTimeout(() => {
      setSafetyScore({
        overall: 0.88,
        toxicity: 0.05,
        environmental_risk: 0.12,
        biocontainment: 0.95,
        recommendations: [
          "Consider adding a kill switch for additional biocontainment",
          "The current design has minimal environmental risk",
        ],
      })
      setActiveTab("safety")

      toast({
        title: "Safety check complete",
        description: "Your design has been analyzed for safety concerns.",
      })
    }, 2000)
  }

  const handleSaveDesign = () => {
    toast({
      title: "Design saved",
      description: "Your design has been saved to your account.",
    })
  }

  const handleShareDesign = () => {
    toast({
      title: "Share options",
      description: "Opening sharing options for your design.",
    })
  }

  const handleExportDesign = () => {
    toast({
      title: "Design exported",
      description: "Your design has been exported as a GenBank file.",
    })
  }

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="container mx-auto py-6 px-4">
        <div className="flex flex-col lg:flex-row gap-6">
          {/* Left Panel - Parts Palette */}
          <div className="w-full lg:w-64 flex-shrink-0">
            <Card>
              <CardContent className="p-4">
                <h2 className="text-lg font-semibold mb-4">DNA Parts</h2>
                <DnaPalette />
              </CardContent>
            </Card>
          </div>

          {/* Center Panel - Design Canvas */}
          <div className="flex-1">
            <div className="flex justify-between items-center mb-4">
              <h1 className="text-2xl font-bold">DNA Circuit Designer</h1>
              <div className="flex gap-2">
                <Button variant="outline" size="sm" onClick={handleSaveDesign}>
                  <Save className="h-4 w-4 mr-2" />
                  Save
                </Button>
                <Button variant="outline" size="sm" onClick={handleShareDesign}>
                  <Share className="h-4 w-4 mr-2" />
                  Share
                </Button>
                <Button variant="outline" size="sm" onClick={handleExportDesign}>
                  <Download className="h-4 w-4 mr-2" />
                  Export
                </Button>
              </div>
            </div>

            <Card className="mb-6">
              <CardContent className="p-4">
                <DnaCanvas sequence={sequence} setSequence={setSequence} />
              </CardContent>
            </Card>

            <Tabs value={activeTab} onValueChange={setActiveTab}>
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="design">Design</TabsTrigger>
                <TabsTrigger value="simulate">Simulation</TabsTrigger>
                <TabsTrigger value="safety">Safety</TabsTrigger>
              </TabsList>

              <TabsContent value="design">
                <Card>
                  <CardContent className="p-4">
                    <div className="h-64">
                      <DnaViewer sequence={sequence} />
                    </div>
                    <Separator className="my-4" />
                    <div className="flex justify-between">
                      <div>
                        <p className="text-sm text-gray-500">
                          {sequence.length} parts | {sequence.reduce((acc, part) => acc + part.length, 0)} base pairs
                        </p>
                      </div>
                      <div className="flex gap-2">
                        <Button onClick={handleSafetyCheck} variant="outline">
                          Safety Check
                        </Button>
                        <Button onClick={handleRunSimulation} className="bg-green-600 hover:bg-green-700">
                          <Play className="h-4 w-4 mr-2" />
                          Run Simulation
                        </Button>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="simulate">
                <SimulationPanel results={simulationResults} />
              </TabsContent>

              <TabsContent value="safety">
                <SafetyPanel score={safetyScore} />
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </div>
    </DndProvider>
  )
}
