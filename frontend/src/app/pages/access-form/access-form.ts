import { Component } from '@angular/core';
import { AdminService } from '../../services/admin.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-access-form',
  imports: [CommonModule, FormsModule],
  templateUrl: './access-form.html'
})
export class AccessFormComponent {
  email = '';
  password = '';
  errorMessage = '';
  showPassword = false;
  isLoading = false;

  constructor(private authService: AdminService) {}

  togglePassword() {
    this.showPassword = !this.showPassword;
  }

  onLogin() {
    if (!this.email || !this.password) {
      this.errorMessage = 'Please enter both email and password';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    this.authService.adminLogin({ email: this.email, password: this.password }).subscribe({
      next: (response: any) => {
        this.isLoading = false;
        console.log('Login successful:', response);
        
        // Redirect to Flask-Admin after successful login
        setTimeout(() => {
          window.location.href = 'http://127.0.0.1:5000/admin';
        }, 100);
      },
      error: (err) => {
        this.isLoading = false;
        console.error('Login error:', err);
        this.errorMessage = err?.error?.error || 'Login failed. Please check your credentials.';
      }
    });
  }
}