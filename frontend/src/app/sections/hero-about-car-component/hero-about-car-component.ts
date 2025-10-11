import {
  Component,
  ElementRef,
  ViewChild,
  AfterViewInit,
  OnDestroy,
  HostListener
} from '@angular/core';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

@Component({
  selector: 'app-hero-about-car',
  templateUrl: './hero-about-car.component.html',
  styleUrls: ['./hero-about-car.component.css']
})
export class HeroAboutCarComponent implements AfterViewInit, OnDestroy {
  @ViewChild('canvas', { static: false }) canvasRef!: ElementRef<HTMLCanvasElement>;
  @ViewChild('modelColumn', { static: false }) modelColumnRef!: ElementRef<HTMLDivElement>;
  @ViewChild('contentColumn', { static: false }) contentColumnRef!: ElementRef<HTMLDivElement>;

  private scene!: THREE.Scene;
  private camera!: THREE.PerspectiveCamera;
  private renderer!: THREE.WebGLRenderer;
  private controls!: OrbitControls;
  private animationId: number | null = null;
  private modelGroup: THREE.Group | null = null;
  private resizeObserver: ResizeObserver | null = null;

  constructor(private host: ElementRef) {}

  ngAfterViewInit(): void {
    gsap.registerPlugin(ScrollTrigger);

    // init three scene and load model
    this.initThree();
    this.loadModel();

    // setup GSAP slide animation (subtle) from hero -> about
    // trigger between start of about section visible to center and top
    const contentEl = this.contentColumnRef?.nativeElement as HTMLElement | null;
    const aboutEl = contentEl?.querySelector('#aboutSection') as HTMLElement | null;

    if (aboutEl) {
      // small horizontal slide while scrolling to about
      gsap.to('#car', {
        x: () => {
          // compute a modest left shift based on viewport width
          const w = window.innerWidth;
          return w > 1024 ? -120 : -40;
        },
        ease: 'none',
        scrollTrigger: {
          trigger: aboutEl,
          start: 'top center',
          end: 'bottom top',
          scrub: 0.6
        },
      });
    }

    // ensure sticky containment: set model column height same as content (hero+about)
    this.syncColumnHeights();

    // resize observer to keep renderer sized to container
    this.resizeObserver = new ResizeObserver(() => this.onResize());
    if (this.modelColumnRef?.nativeElement) {
      this.resizeObserver.observe(this.modelColumnRef.nativeElement);
    }
    if (this.contentColumnRef?.nativeElement) {
      this.resizeObserver.observe(this.contentColumnRef.nativeElement);
    }

    // initial resize to size canvas correctly
    this.onResize();
  }

  ngOnDestroy(): void {
    if (this.animationId) cancelAnimationFrame(this.animationId);
    if (this.renderer) {
      this.renderer.dispose();
    }
    ScrollTrigger.getAll().forEach(st => st.kill());
    if (this.resizeObserver && this.modelColumnRef?.nativeElement) {
      this.resizeObserver.unobserve(this.modelColumnRef.nativeElement);
      this.resizeObserver.disconnect();
    }
  }

  // keep renderer sized to the model container
  private onResize() {
    const canvas = this.canvasRef?.nativeElement;
    const container = this.modelColumnRef?.nativeElement as HTMLElement | null;
    if (!canvas || !container || !this.renderer || !this.camera) return;

    const width = container.clientWidth;
    const height = container.clientHeight;

    // handle device pixel ratio
    const DPR = Math.min(window.devicePixelRatio || 1, 2);
    this.renderer.setPixelRatio(DPR);
    this.renderer.setSize(width, height, false);

    this.camera.aspect = width / height;
    this.camera.updateProjectionMatrix();
  }

  @HostListener('window:resize')
  handleWindowResize() {
    this.onResize();
  }

  private initThree() {
    const canvas = this.canvasRef.nativeElement;
    this.scene = new THREE.Scene();
    this.scene.background = null;

    // create camera with initial aspect; will update on resize
    this.camera = new THREE.PerspectiveCamera(45, 1, 0.1, 10000);
    this.camera.position.set(0, 120, 350);

    // lights
    const ambient = new THREE.AmbientLight(0xffffff, 0.9);
    this.scene.add(ambient);

    const dir = new THREE.DirectionalLight(0xffffff, 1.0);
    dir.position.set(100, 200, 150);
    this.scene.add(dir);

    // renderer
    this.renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: true
    });
    this.renderer.shadowMap.enabled = true;
    this.renderer.setClearColor(0x000000, 0);

    // orbit controls (auto rotate)
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.autoRotate = true;
    this.controls.autoRotateSpeed = 2.0;
    this.controls.enablePan = false;
    this.controls.enableZoom = false;
    this.controls.enableRotate = false;

    this.animate();
  }

  private loadModel() {
    const loader = new GLTFLoader();
    loader.load(
      'assets/model/conceptcar.glb',
      (gltf) => {
        const model = gltf.scene;
        this.processModel(model);
        this.modelGroup = model;

        // center and scale model appropriately
        const box = new THREE.Box3().setFromObject(model);
        const center = box.getCenter(new THREE.Vector3());
        const size = box.getSize(new THREE.Vector3());
        const maxDim = Math.max(size.x, size.y, size.z);

        // compute distance
        const fov = this.camera.fov * (Math.PI / 180);
        let cameraDist = Math.abs(maxDim / 2 / Math.tan(fov / 2));
        cameraDist *= 1.6;

        this.camera.position.set(center.x + cameraDist, center.y + maxDim * 0.25, center.z);
        this.camera.lookAt(center);
        this.controls.target.copy(center);
        this.controls.update();
        this.onResize();
      },
      (xhr) => {
        // optional: you can show progress
        // console.log(`Model ${(xhr.loaded / xhr.total) * 100}%`);
      },
      (err) => console.error('GLTF load error', err)
    );
  }

  private processModel(model: THREE.Object3D) {
    // basic processing: ensure double sided and shadows
    model.scale.set(1, 1, 1);
    model.position.set(0, -10, 0);

    model.traverse((child) => {
      // set mesh material flags
      // @ts-ignore
      if (child.isMesh) {
        const mesh = child as THREE.Mesh;
        mesh.castShadow = true;
        mesh.receiveShadow = true;
        if (Array.isArray(mesh.material)) {
          mesh.material.forEach((m: any) => (m.side = THREE.DoubleSide));
        } else if (mesh.material) {
          (mesh.material as any).side = THREE.DoubleSide;
        }
      }
    });

    this.scene.add(model);
  }

  private animate = () => {
    this.animationId = requestAnimationFrame(this.animate);
    this.controls.update();
    this.renderer.render(this.scene, this.camera);
  };

  // ensure the model column height matches content column (hero + about)
  private syncColumnHeights() {
    const modelCol = this.modelColumnRef?.nativeElement as HTMLElement | null;
    const contentCol = this.contentColumnRef?.nativeElement as HTMLElement | null;
    if (!modelCol || !contentCol) return;

    // set model column min-height to content height so sticky stops at the end
    const contentHeight = contentCol.scrollHeight;
    modelCol.style.minHeight = `${contentHeight}px`;
  }
}
