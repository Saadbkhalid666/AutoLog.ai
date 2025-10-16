import { Component } from '@angular/core';
import { AdminService } from '../../services/admin.service';
@Component({
  selector: 'app-access-form',
  templateUrl: './access-form.html'
})
export class AdminLoginComponent {
  email = '';
  password = '';
  errorMessage = '';

  constructor(private authService: AdminService) {}

  onLogin() {
    this.authService.adminLogin({ email: this.email, password: this.password }).subscribe({
      next: () => {
        window.location.href = 'http://127.0.0.1:5000/admin'; // redirect to flask admin
      },
      error: (err) => {
        this.errorMessage = err?.error?.error || 'Login failed';
      }
    });
  }
}
