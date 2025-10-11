import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from '../services/auth';
@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private auth: AuthService, private router: Router) {
    if (this.auth.getToken()) {
      this.router.navigate(['/']);  
    }
  }
  canActivate(): boolean {
      const token = this.auth.getToken();
      if (token) {
          return true;
        }
        this.router.navigate(['/login']);
        return false;
    }
    
}
