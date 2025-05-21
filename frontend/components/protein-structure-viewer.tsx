"use client"

import { useEffect, useRef, useState } from "react"
import * as THREE from "three"
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls"
import { PDBLoader } from "three/examples/jsm/loaders/PDBLoader"
import { CSS2DRenderer, CSS2DObject } from "three/examples/jsm/renderers/CSS2DRenderer"
import { Button } from "@/components/ui/button"
import { Loader2 } from "lucide-react"

interface ProteinStructureViewerProps {
  pdbData?: string
  width?: number
  height?: number
}

export function ProteinStructureViewer({ pdbData, width = 500, height = 400 }: ProteinStructureViewerProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!containerRef.current || !pdbData) return

    setLoading(true)
    setError(null)

    // Initialize Three.js scene
    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0xf8f9fa)

    // Set up camera
    const camera = new THREE.PerspectiveCamera(70, width / height, 1, 5000)
    camera.position.z = 100

    // Set up renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(width, height)
    containerRef.current.appendChild(renderer.domElement)

    // Set up CSS2D renderer for labels
    const labelRenderer = new CSS2DRenderer()
    labelRenderer.setSize(width, height)
    labelRenderer.domElement.style.position = "absolute"
    labelRenderer.domElement.style.top = "0"
    labelRenderer.domElement.style.pointerEvents = "none"
    containerRef.current.appendChild(labelRenderer.domElement)

    // Set up controls
    const controls = new OrbitControls(camera, renderer.domElement)
    controls.minDistance = 10
    controls.maxDistance = 1000

    // Add lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
    scene.add(ambientLight)

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
    directionalLight.position.set(1, 1, 1)
    scene.add(directionalLight)

    // Create a blob from the PDB data
    const blob = new Blob([pdbData], { type: "text/plain" })
    const url = URL.createObjectURL(blob)

    // Load the PDB file
    const loader = new PDBLoader()
    loader.load(
      url,
      (pdb) => {
        // Create geometry and materials
        const geometryAtoms = pdb.geometryAtoms
        const geometryBonds = pdb.geometryBonds
        const json = pdb.json

        // Create atoms
        const boxGeometry = new THREE.BoxGeometry(1, 1, 1)
        const sphereGeometry = new THREE.IcosahedronGeometry(1, 3)

        const offset = geometryAtoms.center()
        geometryBonds.translate(offset.x, offset.y, offset.z)

        const positions = geometryAtoms.getAttribute("position")
        const colors = geometryAtoms.getAttribute("color")

        const position = new THREE.Vector3()
        const color = new THREE.Color()

        // Create atoms
        for (let i = 0; i < positions.count; i++) {
          position.x = positions.getX(i)
          position.y = positions.getY(i)
          position.z = positions.getZ(i)

          color.r = colors.getX(i)
          color.g = colors.getY(i)
          color.b = colors.getZ(i)

          const material = new THREE.MeshPhongMaterial({ color: color })
          const object = new THREE.Mesh(sphereGeometry, material)
          object.position.copy(position)
          object.position.multiplyScalar(75)
          object.scale.multiplyScalar(25)
          scene.add(object)

          // Add atom label
          const atom = json.atoms[i]
          const text = document.createElement("div")
          text.className = "text-xs bg-black bg-opacity-50 text-white px-1 rounded"
          text.textContent = atom[4]

          const label = new CSS2DObject(text)
          label.position.copy(object.position)
          scene.add(label)
        }

        // Create bonds
        const positionsBonds = geometryBonds.getAttribute("position")

        const start = new THREE.Vector3()
        const end = new THREE.Vector3()

        for (let i = 0; i < positionsBonds.count; i += 2) {
          start.x = positionsBonds.getX(i)
          start.y = positionsBonds.getY(i)
          start.z = positionsBonds.getZ(i)

          end.x = positionsBonds.getX(i + 1)
          end.y = positionsBonds.getY(i + 1)
          end.z = positionsBonds.getZ(i + 1)

          start.multiplyScalar(75)
          end.multiplyScalar(75)

          const bondGeometry = new THREE.CylinderGeometry(5, 5, start.distanceTo(end), 6, 1)
          bondGeometry.translate(0, start.distanceTo(end) / 2, 0)

          const material = new THREE.MeshPhongMaterial({ color: 0xcccccc })
          const mesh = new THREE.Mesh(bondGeometry, material)

          // Position and orient the cylinder
          mesh.position.copy(start)
          mesh.lookAt(end)
          mesh.rotateX(Math.PI / 2)

          scene.add(mesh)
        }

        // Center camera on model
        const boundingBox = new THREE.Box3().setFromObject(scene)
        const center = boundingBox.getCenter(new THREE.Vector3())
        const size = boundingBox.getSize(new THREE.Vector3())
        const maxDim = Math.max(size.x, size.y, size.z)
        const fov = camera.fov * (Math.PI / 180)
        let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2))
        cameraZ *= 1.5 // Zoom out a bit
        camera.position.z = cameraZ
        camera.lookAt(center)
        controls.target.copy(center)

        setLoading(false)
      },
      (xhr) => {
        // Progress callback
        console.log((xhr.loaded / xhr.total) * 100 + "% loaded")
      },
      (error) => {
        // Error callback
        console.error("Error loading PDB:", error)
        setError("Failed to load protein structure")
        setLoading(false)
      },
    )

    // Clean up the URL object
    URL.revokeObjectURL(url)

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate)
      controls.update()
      renderer.render(scene, camera)
      labelRenderer.render(scene, camera)
    }

    animate()

    // Handle window resize
    const handleResize = () => {
      if (!containerRef.current) return

      camera.aspect = width / height
      camera.updateProjectionMatrix()
      renderer.setSize(width, height)
      labelRenderer.setSize(width, height)
    }

    window.addEventListener("resize", handleResize)

    // Cleanup
    return () => {
      window.removeEventListener("resize", handleResize)
      if (containerRef.current) {
        if (renderer.domElement.parentNode) {
          containerRef.current.removeChild(renderer.domElement)
        }
        if (labelRenderer.domElement.parentNode) {
          containerRef.current.removeChild(labelRenderer.domElement)
        }
      }
      scene.clear()
    }
  }, [pdbData, width, height])

  return (
    <div className="relative">
      <div
        ref={containerRef}
        className="w-full h-full rounded-lg overflow-hidden"
        style={{ width: `${width}px`, height: `${height}px` }}
      >
        {loading && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-100 bg-opacity-75">
            <div className="flex flex-col items-center">
              <Loader2 className="h-8 w-8 animate-spin text-green-600" />
              <p className="mt-2 text-sm text-gray-600">Loading protein structure...</p>
            </div>
          </div>
        )}
        {error && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-100">
            <div className="flex flex-col items-center">
              <p className="text-red-500">{error}</p>
              <Button
                variant="outline"
                className="mt-2"
                onClick={() => {
                  setError(null)
                  setLoading(true)
                  // Trigger reload logic here
                }}
              >
                Retry
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
