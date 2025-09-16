import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormGroup, FormControl, Validators, ReactiveFormsModule } from '@angular/forms';
import { AuthService, User } from '../../services/auth'; 

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './signup.html',
  styleUrl: './signup.css',
})
export class Signup {
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

  successMsg = '';
  errorMsg = '';
  loading=false;

  constructor(private authService: AuthService) {}

  Submit() {
    if (this.signupForm.valid) {
      this.loading=true;
      const user: User = this.signupForm.value as User;

      this.authService.signup(user).subscribe({
        next: (res) => {
          this.successMsg = 'Registration Successful!';
          this.errorMsg = '';
          this.loading=false;
          setTimeout(()=>{
            this.successMsg=''
          },3000)
        },
        error: (err) => {
          this.errorMsg = 'SignUp Failed. Please try again.';
          this.successMsg = '';
          this.loading=false;
          setTimeout(()=>{this.errorMsg=''},3000)
        },
      });
    } else {
      this.errorMsg = 'Form is invalid!';
      this.successMsg = '';
    }
  }
}
