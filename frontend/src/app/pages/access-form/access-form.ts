import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Admin } from '../../services/admin.service';

@Component({
  selector: 'app-access-form',
  imports: [CommonModule, FormsModule],
  templateUrl: './access-form.html',
})
export class AccessFormComponent {
  email = '';
  password = '';
  errorMessage = '';
  showPassword = false;
  isLoading = false;

  constructor(private authService: Admin) {}

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
        console.log('✅ Login successful:', response);

        // Add a small delay to ensure session cookie is set
        setTimeout(() => {
          console.log('🔄 Redirecting to Flask-Admin...');
          window.location.href = 'http://127.0.0.1:5000/admin';
        }, 500);
      },
      error: (err) => {
        this.isLoading = false;
        console.error('❌ Login error:', err);
        this.errorMessage = err?.error?.error || 'Login failed. Please check your credentials.';
      },
    });
  }
}
