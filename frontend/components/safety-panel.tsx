"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import { Shield, AlertTriangle, CheckCircle } from "lucide-react"

export function SafetyPanel({ score }) {
  if (!score) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="flex flex-col items-center justify-center h-64">
            <p className="text-gray-500">No safety analysis available</p>
            <p className="text-sm text-gray-400 mt-2">Run a safety check to see results here</p>
          </div>
        </CardContent>
      </Card>
    )
  }

  // Determine overall safety status
  const getSafetyStatus = () => {
    if (score.overall >= 0.8) {
      return {
        icon: <CheckCircle className="h-5 w-5 text-green-500" />,
        title: "Safe Design",
        description: "This design meets safety standards and is suitable for further development.",
        color: "bg-green-50 border-green-200",
      }
    } else if (score.overall >= 0.6) {
      return {
        icon: <AlertTriangle className="h-5 w-5 text-amber-500" />,
        title: "Caution Advised",
        description: "This design has some safety concerns that should be addressed.",
        color: "bg-amber-50 border-amber-200",
      }
    } else {
      return {
        icon: <AlertTriangle className="h-5 w-5 text-red-500" />,
        title: "Safety Concerns",
        description: "This design has significant safety issues that must be resolved.",
        color: "bg-red-50 border-red-200",
      }
    }
  }

  const safetyStatus = getSafetyStatus()

  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-center mb-4">
          <Shield className="h-5 w-5 mr-2 text-blue-500" />
          <h3 className="text-lg font-semibold">Safety Analysis</h3>
        </div>

        <Alert className={`mb-6 ${safetyStatus.color}`}>
          <div className="flex items-start">
            {safetyStatus.icon}
            <div className="ml-3">
              <AlertTitle>{safetyStatus.title}</AlertTitle>
              <AlertDescription>{safetyStatus.description}</AlertDescription>
            </div>
          </div>
        </Alert>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <div>
            <h4 className="text-sm font-medium mb-2">Overall Safety Score</h4>
            <div className="flex items-center">
              <Progress
                value={score.overall * 100}
                className={`h-2 flex-1 ${
                  score.overall >= 0.8 ? "bg-green-100" : score.overall >= 0.6 ? "bg-amber-100" : "bg-red-100"
                }`}
              />
              <span className="ml-2 text-sm font-medium">{Math.round(score.overall * 100)}%</span>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-medium mb-2">Toxicity Risk</h4>
            <div className="flex items-center">
              <Progress value={score.toxicity * 100} className="h-2 flex-1 bg-red-100" />
              <span className="ml-2 text-sm font-medium">{Math.round(score.toxicity * 100)}%</span>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-medium mb-2">Environmental Risk</h4>
            <div className="flex items-center">
              <Progress value={score.environmental_risk * 100} className="h-2 flex-1 bg-amber-100" />
              <span className="ml-2 text-sm font-medium">{Math.round(score.environmental_risk * 100)}%</span>
            </div>
          </div>

          <div>
            <h4 className="text-sm font-medium mb-2">Biocontainment</h4>
            <div className="flex items-center">
              <Progress value={score.biocontainment * 100} className="h-2 flex-1 bg-green-100" />
              <span className="ml-2 text-sm font-medium">{Math.round(score.biocontainment * 100)}%</span>
            </div>
          </div>
        </div>

        <div>
          <h4 className="text-sm font-medium mb-2">Recommendations</h4>
          <ul className="list-disc pl-5 space-y-1">
            {score.recommendations.map((rec, index) => (
              <li key={index} className="text-sm text-gray-600">
                {rec}
              </li>
            ))}
          </ul>
        </div>
      </CardContent>
    </Card>
  )
}
