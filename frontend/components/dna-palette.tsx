"use client"

import { useDrag } from "react-dnd"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

// DNA part types with their colors
const partTypes = {
  promoters: { color: "#FF5757", icon: "→" },
  genes: { color: "#4CAF50", icon: "□" },
  terminators: { color: "#FF9800", icon: "⊣" },
  operators: { color: "#2196F3", icon: "◇" },
  ribosome_binding_sites: { color: "#9C27B0", icon: "○" },
}

// Sample DNA parts for each category
const dnaParts = {
  promoters: [
    { id: "prom1", name: "T7 Promoter", type: "promoters", sequence: "TAATACGACTCACTATAGGG", length: 20 },
    { id: "prom2", name: "Lac Promoter", type: "promoters", sequence: "GAATTGTGAGCGGATAACAATT", length: 22 },
    { id: "prom3", name: "Tet Promoter", type: "promoters", sequence: "TCCCTATCAGTGATAGAGA", length: 19 },
  ],
  genes: [
    { id: "gene1", name: "GFP", type: "genes", sequence: "ATGGTGAGCAAGGGCGAGGAG", length: 120 },
    { id: "gene2", name: "RFP", type: "genes", sequence: "ATGGCCTCCTCCGAGGACGTC", length: 110 },
    { id: "gene3", name: "LacZ", type: "genes", sequence: "ATGACCATGATTACGGATTCA", length: 135 },
  ],
  terminators: [
    { id: "term1", name: "T7 Terminator", type: "terminators", sequence: "CTAGCATAACCCCTTGGGGC", length: 20 },
    { id: "term2", name: "rrnB Terminator", type: "terminators", sequence: "TGCCTGGCGGCAGTAGCGCG", length: 20 },
  ],
  operators: [
    { id: "op1", name: "Lac Operator", type: "operators", sequence: "AATTGTGAGCGGATAACAATT", length: 21 },
    { id: "op2", name: "Tet Operator", type: "operators", sequence: "TCCCTATCAGTGATAGAGA", length: 19 },
  ],
  ribosome_binding_sites: [
    { id: "rbs1", name: "Strong RBS", type: "ribosome_binding_sites", sequence: "AGGAGG", length: 6 },
    { id: "rbs2", name: "Medium RBS", type: "ribosome_binding_sites", sequence: "AGGA", length: 4 },
  ],
}

// DNA Part component
const DnaPart = ({ part }) => {
  const [{ isDragging }, drag] = useDrag(() => ({
    type: "DNA_PART",
    item: part,
    collect: (monitor) => ({
      isDragging: !!monitor.isDragging(),
    }),
  }))

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <div
            ref={drag}
            className="flex items-center p-2 mb-2 rounded border border-gray-200 cursor-move hover:bg-gray-50"
            style={{ opacity: isDragging ? 0.5 : 1 }}
          >
            <div
              className="w-6 h-6 flex items-center justify-center rounded mr-2 text-white"
              style={{ backgroundColor: partTypes[part.type].color }}
            >
              {partTypes[part.type].icon}
            </div>
            <div className="flex-1 overflow-hidden">
              <div className="text-sm font-medium truncate">{part.name}</div>
              <div className="text-xs text-gray-500">{part.length} bp</div>
            </div>
          </div>
        </TooltipTrigger>
        <TooltipContent>
          <p className="font-mono text-xs">{part.sequence.substring(0, 20)}...</p>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}

export function DnaPalette() {
  return (
    <Tabs defaultValue="promoters">
      <TabsList className="grid grid-cols-3 mb-4">
        <TabsTrigger value="promoters">Promoters</TabsTrigger>
        <TabsTrigger value="genes">Genes</TabsTrigger>
        <TabsTrigger value="other">Other</TabsTrigger>
      </TabsList>

      <TabsContent value="promoters">
        <ScrollArea className="h-[400px]">
          {dnaParts.promoters.map((part) => (
            <DnaPart key={part.id} part={part} />
          ))}
        </ScrollArea>
      </TabsContent>

      <TabsContent value="genes">
        <ScrollArea className="h-[400px]">
          {dnaParts.genes.map((part) => (
            <DnaPart key={part.id} part={part} />
          ))}
        </ScrollArea>
      </TabsContent>

      <TabsContent value="other">
        <ScrollArea className="h-[400px]">
          {[...dnaParts.terminators, ...dnaParts.operators, ...dnaParts.ribosome_binding_sites].map((part) => (
            <DnaPart key={part.id} part={part} />
          ))}
        </ScrollArea>
      </TabsContent>
    </Tabs>
  )
}
