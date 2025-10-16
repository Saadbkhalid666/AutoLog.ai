import { CommonModule } from '@angular/common';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-nav',
  standalone: true,
  imports: [CommonModule, RouterLink, RouterLinkActive],
  templateUrl: './nav.html',
  styleUrl: './nav.css',
})
export class Nav implements OnInit, OnDestroy {
  isOpen = false;
  userFirstName: string | null = null;
  name:string | null = null;
  showPanel:boolean = false
  private sub!: Subscription;

  constructor( public authService: AuthService, private router: Router) {}

  ngOnInit() {
    this.sub = this.authService.username$.subscribe((username) => {
      this.userFirstName = username ? username.split(' ')[0] : null;
    });
   this.authService.userRole$.subscribe((role)=>{
    this.showPanel = (role == "admin")
   })

  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

  toggleMenu() {
    this.isOpen = !this.isOpen;
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['login']);
  }
}
