import { Component, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

@Component({
  selector: 'app-home',
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home implements AfterViewInit {
  @ViewChild('canvas', { static: false }) canvasRef!: ElementRef<HTMLCanvasElement>;
  private scene!: THREE.Scene;
  private camera!: THREE.PerspectiveCamera;
  private renderer!: THREE.WebGLRenderer;
  private controls!: OrbitControls;

  ngAfterViewInit() {
    this.initializeScene();
    this.loadModel();
  }

  private initializeScene() {
    const canvas = this.canvasRef.nativeElement;

    // --- Scene ---
    this.scene = new THREE.Scene();
    this.scene.background = null;

    // --- Camera ---
    this.camera = new THREE.PerspectiveCamera(
      45,
      canvas.clientWidth / canvas.clientHeight,
      0.1,
      100000 // Increased far plane to avoid clipping on larger scales
    );
    this.camera.position.set(0, 200, 500);

    // --- Lights ---
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    this.scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(100, 200, 300);
    this.scene.add(directionalLight);

    // --- Renderer ---
    this.renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: true,
    });
    this.renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    this.renderer.shadowMap.enabled = true;
    this.renderer.setClearColor(0x000000, 0);

    // --- Controls ---
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.autoRotate = true; // Enable auto-rotation around the target (model's axis)
    this.controls.autoRotateSpeed = 2.0; // Adjust speed as needed (2.0 is default for reasonable rotation)

    // Start animation loop
    this.animate();
  }

  private loadModel() {
    console.log('🚗 Loading conceptcar.glb...');
    const loader = new GLTFLoader();

    loader.load(
      'assets/model/conceptcar.glb',
      (gltf) => {
        const model = gltf.scene;
        this.processModel(model);

        // --- Fit camera to model ---
        const box = new THREE.Box3().setFromObject(model);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());

        const maxDim = Math.max(size.x, size.y, size.z);
        const fov = this.camera.fov * (Math.PI / 180);
        let cameraDist = Math.abs(maxDim / 2 / Math.tan(fov / 2));

        cameraDist *= 1.5; // Push a bit further to ensure full view without clipping

        // Set initial camera position to view the left side (assuming model oriented with length along x or z; adjust if needed)
        // Here, positioning camera along +x axis to view the model's left side (driver's side if left-hand drive)
        this.camera.position.set(center.x + cameraDist, center.y + maxDim * 0.3, center.z);
        this.camera.lookAt(center);

        this.controls.target.copy(center);
        this.controls.update();

        console.log('✅ conceptcar.glb loaded & camera fitted to left side');
      },
      (xhr) => console.log(`Loading: ${(xhr.loaded / xhr.total * 100).toFixed(2)}%`),
      (error) => console.error('❌ GLTFLoader error:', error)
    );
  }

  private processModel(model: THREE.Group) {
    model.scale.set(1, 1, 1); // Set to normal/original size (adjust if model appears too small/large)
    model.position.y = 0;

    model.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh;
        mesh.castShadow = true;
        mesh.receiveShadow = true;

        if (Array.isArray(mesh.material)) {
          mesh.material.forEach((mat) => {
            (mat as THREE.Material & { side?: THREE.Side }).side = THREE.DoubleSide;
          });
        } else if (mesh.material) {
          (mesh.material as THREE.Material & { side?: THREE.Side }).side = THREE.DoubleSide;
        }
      }
    });

    this.scene.add(model);
  }

  private animate() {
    requestAnimationFrame(() => this.animate());
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  }
}