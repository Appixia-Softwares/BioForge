"use client"

import { useDrop } from "react-dnd"
import { X } from "lucide-react"

// DNA part types with their colors (same as in DnaPalette)
const partTypes = {
  promoters: { color: "#FF5757", icon: "→" },
  genes: { color: "#4CAF50", icon: "□" },
  terminators: { color: "#FF9800", icon: "⊣" },
  operators: { color: "#2196F3", icon: "◇" },
  ribosome_binding_sites: { color: "#9C27B0", icon: "○" },
}

export function DnaCanvas({ sequence, setSequence }) {
  const [{ isOver }, drop] = useDrop(() => ({
    accept: "DNA_PART",
    drop: (item) => {
      // Add the dropped item to the sequence
      setSequence([...sequence, item])
    },
    collect: (monitor) => ({
      isOver: !!monitor.isOver(),
    }),
  }))

  const removePart = (index) => {
    const newSequence = [...sequence]
    newSequence.splice(index, 1)
    setSequence(newSequence)
  }

  return (
    <div
      ref={drop}
      className={`min-h-[200px] p-4 rounded-lg border-2 border-dashed transition-colors ${
        isOver ? "border-green-500 bg-green-50" : "border-gray-300"
      }`}
    >
      {sequence.length === 0 ? (
        <div className="h-full flex items-center justify-center text-gray-400">
          Drag and drop DNA parts here to build your circuit
        </div>
      ) : (
        <div className="flex flex-wrap items-center">
          {sequence.map((part, index) => (
            <div key={`${part.id}-${index}`} className="relative group mr-1 mb-1">
              <div className="flex items-center p-2 rounded border border-gray-200 bg-white">
                <div
                  className="w-6 h-6 flex items-center justify-center rounded mr-2 text-white"
                  style={{ backgroundColor: partTypes[part.type].color }}
                >
                  {partTypes[part.type].icon}
                </div>
                <div className="flex-1">
                  <div className="text-sm font-medium">{part.name}</div>
                  <div className="text-xs text-gray-500">{part.length} bp</div>
                </div>
                <button
                  onClick={() => removePart(index)}
                  className="ml-2 opacity-0 group-hover:opacity-100 transition-opacity"
                >
                  <X className="h-4 w-4 text-gray-400 hover:text-red-500" />
                </button>
              </div>
              {index < sequence.length - 1 && (
                <div className="absolute right-0 top-1/2 transform translate-x-1/2 -translate-y-1/2 w-2 h-0.5 bg-gray-300"></div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
