"use client"
import { Card } from "@/components/ui/card"

export default function ArchitectureDiagram() {
  return (
    <Card className="p-6 bg-white">
      <div className="w-full overflow-auto">
        <div className="min-w-[800px]">
          <svg viewBox="0 0 800 600" className="w-full">
            {/* User Layer */}
            <rect x="350" y="20" width="100" height="40" rx="5" fill="#f0f9ff" stroke="#0ea5e9" strokeWidth="2" />
            <text x="400" y="45" textAnchor="middle" fill="#0f172a" fontSize="14" fontWeight="bold">
              Users
            </text>
            <line x1="400" y1="60" x2="400" y2="90" stroke="#94a3b8" strokeWidth="2" strokeDasharray="5,5" />

            {/* Frontend Layer */}
            <rect x="200" y="90" width="400" height="60" rx="5" fill="#f0f9ff" stroke="#0ea5e9" strokeWidth="2" />
            <text x="400" y="125" textAnchor="middle" fill="#0f172a" fontSize="14" fontWeight="bold">
              Frontend (React + Three.js)
            </text>
            <line x1="400" y1="150" x2="400" y2="180" stroke="#94a3b8" strokeWidth="2" />

            {/* API Gateway */}
            <rect x="300" y="180" width="200" height="40" rx="5" fill="#ecfdf5" stroke="#10b981" strokeWidth="2" />
            <text x="400" y="205" textAnchor="middle" fill="#0f172a" fontSize="14" fontWeight="bold">
              API Gateway (FastAPI)
            </text>

            {/* Backend Services */}
            <line x1="300" y1="220" x2="200" y2="250" stroke="#94a3b8" strokeWidth="2" />
            <line x1="400" y1="220" x2="400" y2="250" stroke="#94a3b8" strokeWidth="2" />
            <line x1="500" y1="220" x2="600" y2="250" stroke="#94a3b8" strokeWidth="2" />

            {/* AI Service */}
            <rect x="100" y="250" width="200" height="60" rx="5" fill="#fef2f2" stroke="#ef4444" strokeWidth="2" />
            <text x="200" y="285" textAnchor="middle" fill="#0f172a" fontSize="14" fontWeight="bold">
              AI Service (ESM-2)
            </text>

            {/* Core Backend */}
            <rect x="320" y="250" width="160" height="60" rx="5" fill="#ecfdf5" stroke="#10b981" strokeWidth="2" />
            <text x="400" y="285" textAnchor="middle" fill="#0f172a" fontSize="14" fontWeight="bold">
              Core Backend
            </text>

            {/* Blockchain Service */}
            <rect x="500" y="250" width="200" height="60" rx="5" fill="#eff6ff" stroke="#3b82f6" strokeWidth="2" />
            <text x="600" y="285" textAnchor="middle" fill="#0f172a" fontSize="14" fontWeight="bold">
              Blockchain (Polygon)
            </text>

            {/* Simulation Engine */}
            <line x1="200" y1="310" x2="200" y2="350" stroke="#94a3b8" strokeWidth="2" />
            <rect x="100" y="350" width="200" height="60" rx="5" fill="#fef2f2" stroke="#ef4444" strokeWidth="2" />
            <text x="200" y="385" textAnchor="middle" fill="#0f172a" fontSize="14" fontWeight="bold">
              Simulation Engine
            </text>

            {/* Data Sources */}
            <line x1="400" y1="310" x2="400" y2="350" stroke="#94a3b8" strokeWidth="2" />
            <rect x="300" y="350" width="200" height="60" rx="5" fill="#ecfdf5" stroke="#10b981" strokeWidth="2" />
            <text x="400" y="375" textAnchor="middle" fill="#0f172a" fontSize="14" fontWeight="bold">
              Data Pipelines
            </text>
            <text x="400" y="395" textAnchor="middle" fill="#0f172a" fontSize="12">
              (GenBank, iGEM Registry)
            </text>

            {/* Safety Layer */}
            <line x1="600" y1="310" x2="600" y2="350" stroke="#94a3b8" strokeWidth="2" />
            <rect x="500" y="350" width="200" height="60" rx="5" fill="#eff6ff" stroke="#3b82f6" strokeWidth="2" />
            <text x="600" y="385" textAnchor="middle" fill="#0f172a" fontSize="14" fontWeight="bold">
              Safety & Biocontainment
            </text>

            {/* Database Layer */}
            <line x1="200" y1="410" x2="200" y2="450" stroke="#94a3b8" strokeWidth="2" />
            <line x1="400" y1="410" x2="400" y2="450" stroke="#94a3b8" strokeWidth="2" />
            <line x1="600" y1="410" x2="600" y2="450" stroke="#94a3b8" strokeWidth="2" />
            <rect x="200" y="450" width="400" height="60" rx="5" fill="#f5f3ff" stroke="#8b5cf6" strokeWidth="2" />
            <text x="400" y="485" textAnchor="middle" fill="#0f172a" fontSize="14" fontWeight="bold">
              Databases & Storage
            </text>

            {/* Legend */}
            <rect x="650" y="500" width="15" height="15" fill="#f0f9ff" stroke="#0ea5e9" strokeWidth="2" />
            <text x="670" y="512" textAnchor="start" fill="#0f172a" fontSize="12">
              Frontend
            </text>

            <rect x="650" y="525" width="15" height="15" fill="#ecfdf5" stroke="#10b981" strokeWidth="2" />
            <text x="670" y="537" textAnchor="start" fill="#0f172a" fontSize="12">
              Backend
            </text>

            <rect x="650" y="550" width="15" height="15" fill="#fef2f2" stroke="#ef4444" strokeWidth="2" />
            <text x="670" y="562" textAnchor="start" fill="#0f172a" fontSize="12">
              AI & Simulation
            </text>

            <rect x="650" y="575" width="15" height="15" fill="#eff6ff" stroke="#3b82f6" strokeWidth="2" />
            <text x="670" y="587" textAnchor="start" fill="#0f172a" fontSize="12">
              Blockchain & Safety
            </text>
          </svg>
        </div>
      </div>
    </Card>
  )
}
