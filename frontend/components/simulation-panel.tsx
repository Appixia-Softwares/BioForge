"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"

// Sample simulation data
const timeSeriesData = [
  { time: 0, growth: 0, protein: 0, metabolite: 0 },
  { time: 2, growth: 0.1, protein: 0.2, metabolite: 0.05 },
  { time: 4, growth: 0.3, protein: 0.4, metabolite: 0.15 },
  { time: 6, growth: 0.5, protein: 0.6, metabolite: 0.3 },
  { time: 8, growth: 0.7, protein: 0.7, metabolite: 0.5 },
  { time: 10, growth: 0.8, protein: 0.8, metabolite: 0.65 },
  { time: 12, growth: 0.85, protein: 0.85, metabolite: 0.75 },
  { time: 14, growth: 0.9, protein: 0.9, metabolite: 0.8 },
  { time: 16, growth: 0.92, protein: 0.92, metabolite: 0.85 },
  { time: 18, growth: 0.94, protein: 0.93, metabolite: 0.88 },
  { time: 20, growth: 0.95, protein: 0.94, metabolite: 0.9 },
]

export function SimulationPanel({ results }) {
  if (!results) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="flex flex-col items-center justify-center h-64">
            <p className="text-gray-500">No simulation results available</p>
            <p className="text-sm text-gray-400 mt-2">Run a simulation to see results here</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardContent className="p-6">
        <h3 className="text-lg font-semibold mb-4">Simulation Results</h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <h4 className="text-sm font-medium mb-2">Growth Rate</h4>
            <div className="flex items-center">
              <Progress value={results.growth_rate * 100} className="h-2 flex-1" />
              <span className="ml-2 text-sm font-medium">{Math.round(results.growth_rate * 100)}%</span>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-medium mb-2">Protein Expression</h4>
            <div className="flex items-center">
              <Progress value={results.protein_expression * 100} className="h-2 flex-1" />
              <span className="ml-2 text-sm font-medium">{Math.round(results.protein_expression * 100)}%</span>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-medium mb-2">Metabolic Burden</h4>
            <div className="flex items-center">
              <Progress value={results.metabolic_burden * 100} className="h-2 flex-1" />
              <span className="ml-2 text-sm font-medium">{Math.round(results.metabolic_burden * 100)}%</span>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-medium mb-2">Stability</h4>
            <div className="flex items-center">
              <Progress value={results.stability * 100} className="h-2 flex-1" />
              <span className="ml-2 text-sm font-medium">{Math.round(results.stability * 100)}%</span>
            </div>
          </div>
        </div>

        <Tabs defaultValue="growth">
          <TabsList className="grid grid-cols-3 mb-4">
            <TabsTrigger value="growth">Growth</TabsTrigger>
            <TabsTrigger value="protein">Protein</TabsTrigger>
            <TabsTrigger value="metabolite">Metabolite</TabsTrigger>
          </TabsList>

          <TabsContent value="growth">
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={timeSeriesData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" label={{ value: "Time (hours)", position: "insideBottom", offset: -5 }} />
                  <YAxis label={{ value: "Growth", angle: -90, position: "insideLeft" }} />
                  <Tooltip />
                  <Line type="monotone" dataKey="growth" stroke="#4CAF50" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </TabsContent>

          <TabsContent value="protein">
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={timeSeriesData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" label={{ value: "Time (hours)", position: "insideBottom", offset: -5 }} />
                  <YAxis label={{ value: "Protein", angle: -90, position: "insideLeft" }} />
                  <Tooltip />
                  <Line type="monotone" dataKey="protein" stroke="#2196F3" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </TabsContent>

          <TabsContent value="metabolite">
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={timeSeriesData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" label={{ value: "Time (hours)", position: "insideBottom", offset: -5 }} />
                  <YAxis label={{ value: "Metabolite", angle: -90, position: "insideLeft" }} />
                  <Tooltip />
                  <Line type="monotone" dataKey="metabolite" stroke="#FF9800" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}
