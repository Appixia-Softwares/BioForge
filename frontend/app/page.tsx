import { Button } from "@/components/ui/button"
import Link from "next/link"
import { ArrowRight, Dna, Globe, Shield } from "lucide-react"

export default function HomePage() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* Hero Section */}
      <section className="py-20 px-4 bg-gradient-to-b from-green-50 to-white">
        <div className="container mx-auto max-w-6xl">
          <div className="flex flex-col md:flex-row items-center gap-12">
            <div className="flex-1 space-y-6">
              <h1 className="text-5xl font-bold tracking-tight text-green-900">
                Design Synthetic Biology <br />
                <span className="text-green-600">Without Code</span>
              </h1>
              <p className="text-xl text-gray-600 max-w-xl">
                BioForge empowers citizen scientists to create and simulate synthetic organisms that solve global
                sustainability challenges.
              </p>
              <div className="flex gap-4 pt-4">
                <Button asChild size="lg" className="bg-green-600 hover:bg-green-700">
                  <Link href="/designer">
                    Start Designing <ArrowRight className="ml-2 h-5 w-5" />
                  </Link>
                </Button>
                <Button asChild variant="outline" size="lg">
                  <Link href="/learn">Learn More</Link>
                </Button>
              </div>
            </div>
            <div className="flex-1 flex justify-center">
              <div className="w-full max-w-md h-80 bg-white rounded-xl shadow-lg overflow-hidden">
                {/* Placeholder for 3D DNA visualization */}
                <div className="w-full h-full bg-gradient-to-br from-green-100 to-blue-100 flex items-center justify-center">
                  <Dna className="w-32 h-32 text-green-500" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-6xl">
          <h2 className="text-3xl font-bold text-center mb-16">How BioForge Works</h2>

          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition">
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
                <Dna className="h-6 w-6 text-green-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Design DNA Circuits</h3>
              <p className="text-gray-600">
                Drag and drop genetic parts to create custom organisms with our intuitive no-code interface.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition">
              <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                <Shield className="h-6 w-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">AI Safety Validation</h3>
              <p className="text-gray-600">
                Our AI ensures your designs are safe, functional, and optimized for your target application.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 hover:shadow-md transition">
              <div className="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                <Globe className="h-6 w-6 text-purple-600" />
              </div>
              <h3 className="text-xl font-semibold mb-2">Simulate & Share</h3>
              <p className="text-gray-600">
                Test your designs in our simulation engine and share them with the community via blockchain.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
