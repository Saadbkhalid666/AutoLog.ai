import { CommonModule } from '@angular/common';
import { Component, HostListener, ElementRef, AfterViewInit } from '@angular/core';
import { Services } from '../../sections/services/services';

@Component({
  selector: 'app-home',
  imports:[CommonModule,Services],
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
