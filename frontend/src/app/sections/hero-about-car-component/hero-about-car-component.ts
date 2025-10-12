import { CommonModule } from '@angular/common';
import { AfterViewInit, Component, ViewChild, ElementRef, HostListener } from '@angular/core';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

@Component({
  selector: 'app-hero-about-car',
  imports: [CommonModule],
  templateUrl: './hero-about-car-component.html',
  styleUrl: './hero-about-car-component.css'
})
export class HeroAboutCarComponent implements AfterViewInit {

  @ViewChild('canvas', { static: false }) canvasRef!: ElementRef<HTMLCanvasElement>;
  private scene!: THREE.Scene;
  private camera!: THREE.PerspectiveCamera;
  private renderer!: THREE.WebGLRenderer;
  private controls!: OrbitControls;
  private carModel!: THREE.Group;
  private carPosition = { x: 200, y: 0, z: 0 }; // Start on right side

  ngAfterViewInit() {
    this.initializeScene();
    this.loadModel();
    gsap.registerPlugin(ScrollTrigger);
    
    this.setupScrollAnimation();
    
    window.addEventListener('resize', () => this.onWindowResize());
  }

  private initializeScene() {
    const canvas = this.canvasRef.nativeElement;
    this.scene = new THREE.Scene();
    this.scene.background = null;

    this.camera = new THREE.PerspectiveCamera(
      45,
      canvas.clientWidth / canvas.clientHeight,
      0.1,
      10000
    );
    this.camera.position.set(0, 200, 500);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    this.scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(100, 200, 300);
    this.scene.add(directionalLight);

    this.renderer = new THREE.WebGLRenderer({ 
      canvas, 
      antialias: true, 
      alpha: true 
    });
    this.renderer.setSize(canvas.clientWidth, canvas.clientHeight);
    this.renderer.shadowMap.enabled = true;
    this.renderer.setClearColor(0x000000, 0);

    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.autoRotate = true;
    this.controls.autoRotateSpeed = 2.0;
    this.controls.enablePan = false;
    this.controls.enableZoom = false;
    this.controls.enableRotate = false;
  }

  private loadModel() {
    const loader = new GLTFLoader();
    loader.load(
      'assets/model/conceptcar.glb',
      (gltf) => {
        this.carModel = gltf.scene;
        this.processModel(this.carModel);

        // Position car on right side initially
        this.carModel.position.set(this.carPosition.x, this.carPosition.y, this.carPosition.z);

        const box = new THREE.Box3().setFromObject(this.carModel);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);
        const fov = this.camera.fov * (Math.PI / 180);
        let cameraDist = Math.abs(maxDim / 2 / Math.tan(fov / 2));
        cameraDist *= 1.5;

        this.camera.position.set(center.x, center.y + maxDim * 0.3, center.z + cameraDist);
        this.camera.lookAt(center);
        this.controls.target.copy(center);
        this.controls.update();

        this.animate();
      },
      (xhr) => console.log(`Loading: ${((xhr.loaded / xhr.total) * 100).toFixed(2)}%`),
      (error) => console.error('❌ GLTFLoader error:', error)
    );
  }

  private processModel(model: THREE.Group) {
    model.scale.set(1, 1, 1);
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

  private setupScrollAnimation() {
    // Animate the car model position based on scroll
    gsap.to(this.carPosition, {
      x: -200, // Move to left side
      ease: "power2.inOut",
      scrollTrigger: {
        trigger: "#about",
        start: "top bottom",
        end: "bottom top",
        scrub: true, // Smoothly follows scroll position
        onUpdate: () => {
          // Update car position when scroll updates
          if (this.carModel) {
            this.carModel.position.x = this.carPosition.x;
          }
        }
      }
    });

    // Optional: Add some rotation animation during scroll
    if (this.carModel) {
      gsap.to(this.carModel.rotation, {
        y: Math.PI * 0.5, // Rotate 90 degrees during scroll
        ease: "power2.inOut",
        scrollTrigger: {
          trigger: "#about",
          start: "top bottom",
          end: "bottom top",
          scrub: true
        }
      });
    }
  }

  private animate() {
    requestAnimationFrame(() => this.animate());
    
    // Update controls and camera if needed
    this.controls.update();
    
    // Render the scene
    this.renderer.render(this.scene, this.camera);
  }

  @HostListener('window:resize')
  private onWindowResize() {
    const canvas = this.canvasRef.nativeElement;
    this.camera.aspect = canvas.clientWidth / canvas.clientHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(canvas.clientWidth, canvas.clientHeight);
  }
}