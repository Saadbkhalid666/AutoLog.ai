import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService } from '../../services/admin.service';

@Component({
  selector: 'app-access-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './access-form.html',
  styleUrls: ['./access-form.css']
})
export class AccessFormComponent {
  email = '';
  password = '';
  errorMessage = '';
  showPassword = false;
  isLoading = false;

  constructor(private adminService: AdminService) {}

  togglePassword(): void {
    this.showPassword = !this.showPassword;
  }

  onLogin(): void {
    if (!this.email || !this.password) {
      this.errorMessage = 'Please enter both email and password.';
      return;
    }

    this.isLoading = true;
    this.errorMessage = '';

    this.adminService.adminLogin({ email: this.email, password: this.password }).subscribe({
      next: (response) => {
        console.log('✅ Login successful:', response);
        this.isLoading = false;

        // Small delay to allow session cookie to set
        setTimeout(() => {
          console.log('🔄 Redirecting to Flask-Admin UI...');
          window.location.href = 'http://127.0.0.1:5000/admin';
        }, 500);
      },
      error: (err) => {
        console.error('❌ Login error:', err);
        this.isLoading = false;
        this.errorMessage =
          err?.error?.error || 'Login failed. Please check your credentials.';
      }
    });
  }
}
