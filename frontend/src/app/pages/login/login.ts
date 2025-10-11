import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService, User } from '../../services/auth';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-login',
  imports: [CommonModule, ReactiveFormsModule,RouterLink],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class Login {
  toasts: { message: string; type: 'success' | 'error' }[] = [];
  loading = false;
  passwordVisible = false;

  loginForm = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', [Validators.required, Validators.minLength(6)])
  });

  constructor(private authService: AuthService, private router: Router) {}

  get email() { return this.loginForm.get('email'); }
  get password() { return this.loginForm.get('password'); }

  togglePassword() {
    this.passwordVisible = !this.passwordVisible;
  }

  showToast(message: string, type: 'success' | 'error' = 'success') {
    const toast = { message, type };
    this.toasts.push(toast);
    setTimeout(() => {
      this.toasts = this.toasts.filter(t => t !== toast);
    }, 3000);
  }

  Submit() {
    if (!this.loginForm.valid) {
      this.showToast('Form is invalid!', 'error');
      return;
    }

    this.loading = true;
    const credentials = this.loginForm.value as User;

    this.authService.login(credentials).subscribe({
      next: res => {
        this.loginForm.reset();
        this.loading = false;
        this.showToast('Login Successful!', 'success');
        this.router.navigate(['home']);
      },
      error: err => {
        this.loading = false;
        const msg = err?.error?.message || 'Login Failed. Try again!';
        this.showToast(msg, 'error');
      }
    });
  }
}
