import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormArray, FormControl, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth'; 
import { Router } from '@angular/router';

@Component({
  selector: 'app-otp',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './otp.html',
  styleUrls: ['./otp.css']
})
export class Otp {
  toasts: { message: string; type: 'success' | 'error' }[] = [];
  loading = false;

  otpForm: FormGroup<{ digits: FormArray<FormControl<string | null>> }>;

  constructor(private fb: FormBuilder, private authService: AuthService, private router: Router) {
    this.otpForm = this.fb.group({
      digits: this.fb.array<FormControl<string | null>>(
        Array(6).fill('').map(() => new FormControl('', { nonNullable: false }))
      )
    });
  }

  get digits(): FormArray<FormControl<string | null>> {
    return this.otpForm.get('digits') as FormArray<FormControl<string | null>>;
  }

  getControl(index: number): FormControl<string | null> {
    return this.digits.at(index) as FormControl<string | null>;
  }

  onInput(event: any, index: number) {
    const input = event.target as HTMLInputElement;
    if (input.value.length === 1 && index < this.digits.length - 1) {
      const nextInput = input.parentElement?.children[index + 1] as HTMLInputElement;
      nextInput.focus();
    }
  }

  onKeyDown(event: KeyboardEvent, index: number) {
    if (event.key === 'Backspace' && !this.getControl(index).value && index > 0) {
      const prevInput = (event.target as HTMLInputElement).parentElement?.children[index - 1] as HTMLInputElement;
      prevInput.focus();
    }
  }

  getOtp(): string {
    return this.digits.value.join('');
  }

  showToast(message: string, type: 'success' | 'error' = 'success') {
    const toast = { message, type };
    this.toasts.push(toast);
    setTimeout(() => {
      this.toasts = this.toasts.filter(t => t !== toast);
    }, 3000);
  }

  onSubmit() {
    if (!this.otpForm.valid) {
      this.showToast('Form is invalid!', 'error');
      return;
    }

    this.loading = true;
    const otp = this.getOtp();

    this.authService.verifyOtp({ otp }).subscribe({
      next: res => {
        this.loading = false;
        this.showToast('OTP Verified Successfully!', 'success');
        this.otpForm.reset();
        this.router.navigate(['login']);
      },
      error: err => {
        this.loading = false;
        const msg = err?.error?.message || 'Invalid OTP. Try again!';
        this.showToast(msg, 'error');
      }
    });
  }
}
