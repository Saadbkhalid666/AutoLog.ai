import { Component, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

@Component({
  selector: 'app-model',
  templateUrl: './model.html',
  styleUrls: ['./model.css'],
})
export class Model implements AfterViewInit {
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

    // --- Scene & Camera ---
    this.scene = new THREE.Scene();
    this.scene.background = null;

    this.camera = new THREE.PerspectiveCamera(
      45,
      canvas.clientWidth / canvas.clientHeight,
      0.1,
      5000
    );
    this.camera.position.set(0, 50, 300);

    // --- Lights ---
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    this.scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(100, 200, 100);
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

    // Start animation loop
    this.animate();
  }

  private loadModel() {
    console.log('🚗 Loading conceptcar.glb...');
    const loader = new GLTFLoader();

    loader.load(
      'assets/model/conceptcar.glb', // ✅ direct path to your .glb
      (gltf) => {
        this.processModel(gltf.scene);
        console.log('✅ conceptcar.glb loaded successfully');
      },
      (xhr) => {
        console.log(`Loading: ${(xhr.loaded / xhr.total * 100).toFixed(2)}%`);
      },
      (error) => {
        console.error('❌ GLTFLoader error:', error);
      }
    );
  }

  private processModel(model: THREE.Group) {
    model.scale.set(5, 5, 5);
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
