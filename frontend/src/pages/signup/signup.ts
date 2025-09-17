import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormGroup, FormControl, Validators, ReactiveFormsModule } from '@angular/forms';
import { AuthService, User } from '../../services/auth';

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
    }, 3000); // match with CSS animation
  }

  signupForm = new FormGroup({
    username: new FormControl<string>('', [Validators.required, Validators.minLength(3)]),
    email: new FormControl<string>('', [Validators.required, Validators.email]),
    password: new FormControl<string>('', [Validators.required, Validators.minLength(6)]),
  });

  get username() { return this.signupForm.get('username'); }
  get email() { return this.signupForm.get('email'); }
  get password() { return this.signupForm.get('password'); }

  loading = false;

  constructor(private authService: AuthService) {}

  Submit() {
    if (this.signupForm.valid) {
      this.loading = true;
      const user: User = this.signupForm.value as User;

      this.authService.signup(user).subscribe({
        next: () => {
          this.signupForm.reset();
          this.showToast('Registration Successful!', 'success');
          this.loading = false;
        },
        error: () => {
          this.showToast('Registration Failed. Try again!', 'error');
          this.loading = false;
        },
      });
    } else {
      this.showToast('Form is invalid!', 'error');
    }
  }
}
