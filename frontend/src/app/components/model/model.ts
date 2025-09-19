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

  ngAfterViewInit() {
    const canvas = this.canvasRef.nativeElement;

    // Scene
    const scene = new THREE.Scene();

    // Camera
    const camera = new THREE.PerspectiveCamera(
      40,
      canvas.clientWidth / canvas.clientHeight,
      0.1,
      5000
    );
    camera.position.set(0, 100, 800);

    // Lights
    scene.add(new THREE.AmbientLight(0xffffff, 1));

    const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
    directionalLight.position.set(0, 1, 0);
    scene.add(directionalLight);

    const pointLight1 = new THREE.PointLight(0x4c4c4c, 1, 1000);
    pointLight1.position.set(0, 300, 500);
    scene.add(pointLight1);

    const pointLight2 = new THREE.PointLight(0x4c4c4c, 1, 1000);
    pointLight2.position.set(200, 100, 0);
    scene.add(pointLight2);

    const pointLight3 = new THREE.PointLight(0x4c4c4c, 1, 1000);
    pointLight3.position.set(-200, 100, 0);
    scene.add(pointLight3);

    const pointLight4 = new THREE.PointLight(0x4c4c4c, 1, 1000);
    pointLight4.position.set(0, -100, -200);
    scene.add(pointLight4);

    // Renderer
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
    renderer.setSize(canvas.clientWidth, canvas.clientHeight);

    // Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;

    // Load Model
    const loader = new GLTFLoader();
    loader.load('/scene.gltf', (gltf) => {
      const model = gltf.scene;
      model.scale.set(0.5, 0.5, 0.5);
      scene.add(model);
    });

    // Animation loop
    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };
    animate();
  }
}