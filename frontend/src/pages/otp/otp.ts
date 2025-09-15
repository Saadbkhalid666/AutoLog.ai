import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormArray, FormControl, ReactiveFormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth'; // path adjust karna ho sakta hai

@Component({
  selector: 'app-otp',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './otp.html',
  styleUrls: ['./otp.css']
})
export class Otp {
  otpForm: FormGroup<{ digits: FormArray<FormControl<string | null>> }>;
  loading = false;
  err = "";
  success = "";
  constructor(private fb: FormBuilder, private authService: AuthService) {
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

  onSubmit() {
    if (this.otpForm.valid) {
      this.loading = true;
      const otp = this.getOtp();

      this.authService.verifyOtp({ otp }).subscribe({
        next: (res) => {
          this.loading = false;
          this.success = "OTP Verified Successfully!";
          this.err = "";
        },
        error: (err) => {
          this.err = "OTP Verification Failed.";
          this.success = "";
          this.loading = false;
        }
      });
    } else {
      console.error('Form is invalid!');
    }
  }
}
