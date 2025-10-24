import { Component } from '@angular/core';
import { AdminService } from '../../services/admin.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-access-form',
  imports:[CommonModule, FormsModule],
  templateUrl: './access-form.html'
})
export class AccessFormComponent {
  email = '';
  password = '';
  errorMessage = '';

  constructor(private authService: AdminService) {}
showPassword = false;

togglePassword() {
  this.showPassword = !this.showPassword;
}

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
