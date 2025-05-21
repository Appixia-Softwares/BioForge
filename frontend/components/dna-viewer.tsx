"use client"

import { useEffect, useRef } from "react"
import * as THREE from "three"
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls"

// DNA part types with their colors (same as in DnaPalette)
const partTypes = {
  promoters: { color: "#FF5757" },
  genes: { color: "#4CAF50" },
  terminators: { color: "#FF9800" },
  operators: { color: "#2196F3" },
  ribosome_binding_sites: { color: "#9C27B0" },
}

export function DnaViewer({ sequence }) {
  const containerRef = useRef(null)
  const sceneRef = useRef(null)

  useEffect(() => {
    if (!containerRef.current) return

    // Initialize Three.js scene
    const width = containerRef.current.clientWidth
    const height = containerRef.current.clientHeight

    const scene = new THREE.Scene()
    scene.background = new THREE.Color(0xf8f9fa)

    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)
    camera.position.z = 5

    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setSize(width, height)
    containerRef.current.appendChild(renderer.domElement)

    const controls = new OrbitControls(camera, renderer.domElement)
    controls.enableDamping = true

    // Add ambient light
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6)
    scene.add(ambientLight)

    // Add directional light
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
    directionalLight.position.set(1, 1, 1)
    scene.add(directionalLight)

    // Store scene reference for cleanup
    sceneRef.current = { scene, camera, renderer, controls }

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate)
      controls.update()
      renderer.render(scene, camera)
    }

    animate()

    // Handle window resize
    const handleResize = () => {
      if (!containerRef.current) return

      const width = containerRef.current.clientWidth
      const height = containerRef.current.clientHeight

      camera.aspect = width / height
      camera.updateProjectionMatrix()
      renderer.setSize(width, height)
    }

    window.addEventListener("resize", handleResize)

    // Cleanup
    return () => {
      window.removeEventListener("resize", handleResize)
      if (containerRef.current && renderer.domElement) {
        containerRef.current.removeChild(renderer.domElement)
      }
    }
  }, [])

  // Update DNA visualization when sequence changes
  useEffect(() => {
    if (!sceneRef.current || !sequence) return

    const { scene } = sceneRef.current

    // Clear previous DNA model
    scene.children = scene.children.filter(
      (child) => child instanceof THREE.Light || child instanceof THREE.AmbientLight,
    )

    if (sequence.length === 0) return

    // Create DNA backbone
    const backboneGeometry = new THREE.CylinderGeometry(0.05, 0.05, sequence.length * 0.5, 8)
    const backboneMaterial = new THREE.MeshStandardMaterial({ color: 0xdddddd })
    const backbone = new THREE.Mesh(backboneGeometry, backboneMaterial)
    scene.add(backbone)

    // Add DNA parts as colored segments
    let offset = -sequence.length * 0.25
    sequence.forEach((part) => {
      const partLength = part.length * 0.01
      const partGeometry = new THREE.CylinderGeometry(0.2, 0.2, partLength, 16)
      const partMaterial = new THREE.MeshStandardMaterial({
        color: new THREE.Color(partTypes[part.type].color),
        transparent: true,
        opacity: 0.8,
      })

      const partMesh = new THREE.Mesh(partGeometry, partMaterial)
      partMesh.position.y = offset + partLength / 2
      scene.add(partMesh)

      offset += partLength
    })
  }, [sequence])

  return <div ref={containerRef} className="w-full h-full" />
}
