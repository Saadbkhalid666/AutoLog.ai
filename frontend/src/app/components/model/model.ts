import { Component, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js';

@Component({
  selector: 'app-model',
  templateUrl: './model.html',
  styleUrls: ['./model.css'],
})
export class Model implements AfterViewInit {
  @ViewChild('canvas', { static: false }) canvasRef!: ElementRef<HTMLCanvasElement>;

  ngAfterViewInit() {
    const canvas = this.canvasRef.nativeElement;

    // --- Scene & Camera ---
    const scene = new THREE.Scene();
    scene.background = null; // transparent background

    const camera = new THREE.PerspectiveCamera(
      45,
      canvas.clientWidth / canvas.clientHeight,
      0.1,
      5000
    );
    camera.position.set(0, 50, 300);

    // --- Lights ---
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(100, 200, 100);
    scene.add(directionalLight);

    // --- Renderer ---
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    renderer.shadowMap.enabled = true;
    renderer.setClearColor(0x000000, 0); // fully transparent

    // --- Controls ---
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // --- GLTF Loader with optional Draco compression support ---
    const gltfLoader = new GLTFLoader();
    
    // Optional: Add Draco compression support if your GLTF uses it
    const dracoLoader = new DRACOLoader();
    dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.6/');
    gltfLoader.setDRACOLoader(dracoLoader);

    const gltfPath = '/assets/model/scene.gltf'; // Update path to your GLTF file

    gltfLoader.load(
      gltfPath,
      (gltf) => {
        const model = gltf.scene;
        
        // Scale and position the model
        model.scale.set(5, 5, 5);
        model.position.y = 0;

        // Configure materials and shadows
        model.traverse((child) => {
          if ((child as THREE.Mesh).isMesh) {
            const mesh = child as THREE.Mesh;
            mesh.castShadow = true;
            mesh.receiveShadow = true;

            // Make materials double-sided if needed
            if (Array.isArray(mesh.material)) {
              mesh.material.forEach((mat) => {
                (mat as THREE.Material & { side?: THREE.Side }).side = THREE.DoubleSide;
              });
            } else if (mesh.material) {
              (mesh.material as THREE.Material & { side?: THREE.Side }).side = THREE.DoubleSide;
            }
          }
        });

        scene.add(model);
        
        // Optional: If you want to automatically center the model
        this.centerModel(model, camera, controls);
      },
      (xhr) => {
        // Loading progress (optional)
        console.log((xhr.loaded / xhr.total * 100) + '% loaded');
      },
      (error) => {
        console.error('Error loading GLTF:', error);
      }
    );

    // --- Animate ---
    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();
  }

  // Helper method to center the model in view
  private centerModel(model: THREE.Group, camera: THREE.PerspectiveCamera, controls: OrbitControls) {
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    
    const maxDim = Math.max(size.x, size.y, size.z);
    const fov = camera.fov * (Math.PI / 180);
    let cameraZ = Math.abs(maxDim / Math.sin(fov / 2));
    
    // Add some padding
    cameraZ *= 1.5;
    
    camera.position.set(center.x, center.y, cameraZ);
    camera.lookAt(center);
    controls.target.copy(center);
    controls.update();
  }
}