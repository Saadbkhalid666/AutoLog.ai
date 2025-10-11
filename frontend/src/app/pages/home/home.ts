import { CommonModule } from '@angular/common';
import { Component, HostListener, ElementRef, AfterViewInit } from '@angular/core';
import { CarModel } from '../../components/car-model/car-model';
import { Hero } from '../../sections/hero/hero';
import { About } from '../../sections/about/about';
import { Services } from '../../sections/services/services';

@Component({
  selector: 'app-home',
  imports:[CommonModule, CarModel, Hero, About,Services],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class Home implements AfterViewInit {
  isStuck: boolean = true;
  aboutOffsetTop: number = 0;

  constructor(private el: ElementRef) {}

  ngAfterViewInit() {
    const aboutSection = this.el.nativeElement.querySelector('#aboutSection');
    this.aboutOffsetTop = aboutSection.offsetTop;
  }

  @HostListener('window:scroll', [])
  onScroll() {
    const scrollPos = window.scrollY;
    this.isStuck = scrollPos < this.aboutOffsetTop - 200; // adjust threshold if needed
  }
}
