import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormGroup, FormControl, Validators, ReactiveFormsModule } from '@angular/forms';
import { AuthService, User } from '../../services/auth';
import { Router, RouterLink } from '@angular/router';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './signup.html',
  styleUrls: ['./signup.css'],
})
export class Signup {
  toasts: { message: string; type: 'success' | 'error' }[] = [];
  loading = false;
  passwordVisible = false;

  signupForm = new FormGroup({
    username: new FormControl<string>('', [Validators.required, Validators.minLength(3)]),
    email: new FormControl<string>('', [Validators.required, Validators.email]),
    password: new FormControl<string>('', [Validators.required, Validators.minLength(6)]),
  });

  constructor(private authService: AuthService, private router: Router) {}

  get username() { return this.signupForm.get('username'); }
  get email() { return this.signupForm.get('email'); }
  get password() { return this.signupForm.get('password'); }

  togglePassword() {
    this.passwordVisible = !this.passwordVisible;
  }

  showToast(message: string, type: 'success' | 'error' = 'success') {
    const toast = { message, type };
    this.toasts.push(toast);
    setTimeout(() => this.toasts = this.toasts.filter(t => t !== toast), 3000);
  }

  Submit() {
    if (!this.signupForm.valid) {
      this.showToast('Form is invalid!', 'error');
      return;
    }

    this.loading = true;
    const user: User = this.signupForm.value as User;

    this.authService.signup(user).subscribe({
      next: () => {
        this.loading = false;
        this.signupForm.reset({}, { emitEvent: false });
        this.showToast('Registration successful! Please verify OTP.', 'success');
        this.router.navigate(['verify-otp']);
      },
      error: err => {
        this.loading = false;
        const errorMsg = err?.error?.error || err?.error?.message || 'Registration failed. Try again!';
        this.showToast(errorMsg, 'error');
      }
    });
  }
}
