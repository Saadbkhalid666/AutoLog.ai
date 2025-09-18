import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormGroup, FormControl, Validators, ReactiveFormsModule } from '@angular/forms';
import { AuthService, User } from '../../services/auth';
import { Router } from '@angular/router';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './signup.html',
  styleUrls: ['./signup.css'],
})
export class Signup {
  toasts: { message: string; type: 'success' | 'error' }[] = [];

  showToast(message: string, type: 'success' | 'error' = 'success') {
    const toast = { message, type };
    this.toasts.push(toast);

    setTimeout(() => {
      this.toasts = this.toasts.filter((t) => t !== toast);
    }, 3000);
  }

  signupForm = new FormGroup({
    username: new FormControl<string>('', [Validators.required, Validators.minLength(3)]),
    email: new FormControl<string>('', [Validators.required, Validators.email]),
    password: new FormControl<string>('', [Validators.required, Validators.minLength(6)]),
  });

  get username() {
    return this.signupForm.get('username');
  }
  get email() {
    return this.signupForm.get('email');
  }
  get password() {
    return this.signupForm.get('password');
  }

  loading = false;

  constructor(private authService: AuthService, private router: Router) {}

  Submit() {
  if (this.signupForm.valid) {
    this.loading = true;
    const user: User = this.signupForm.value as User;

    this.authService.signup(user).subscribe({
      next: () => {
        this.signupForm.reset({}, { emitEvent: false });
        this.showToast('Registration Successful! Please verify OTP.', 'success');
        this.loading = false;
        this.router.navigate(['verify-otp']);
      },
      error: (err) => {
        this.loading = false;
        if (err.error?.error === 'User already registered') {
          this.showToast('User is already registered!', 'error');
        } else if (err.error?.error === 'Username already taken') {
          this.showToast('Username already taken!', 'error');
        } else if (err.error?.message) {
          this.showToast(err.error.message, 'error');
        } else {
          this.showToast('Registration Failed. Try again!', 'error');
        }
      },
    });
  } else {
    this.showToast('Form is invalid!', 'error');
  }
}

}
