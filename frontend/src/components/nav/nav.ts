import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-nav',
  imports: [CommonModule],
  templateUrl: './nav.html',
  styleUrl: './nav.css'
})
export class Nav {
isOpen = false;  

  toggleMenu() {
    this.isOpen = !this.isOpen;
  }
}
