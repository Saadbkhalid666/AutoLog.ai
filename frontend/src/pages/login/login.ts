import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthService, User } from '../../services/auth';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css'
})
export class Login {
 toasts: { message: string; type: 'success' | 'error' }[] = [];

  showToast(message: string, type: 'success' | 'error' = 'success') {
    const toast = { message, type };
    this.toasts.push(toast);

    setTimeout(() => {
      this.toasts = this.toasts.filter((t) => t !== toast);
    }, 3000); // match with CSS animation
  }

  loginForm =  new FormGroup({
    email: new FormControl('',Validators.email),
    password: new FormControl('',Validators.minLength(6))
  })
  get email( ){return this.loginForm.get('email')}
  get password( ){return this.loginForm.get('password')}

  constructor(private authService: AuthService, private router: Router) {}
  loading = false;
  Submit() {
    if(this.loginForm.valid){
      this.loading = true;
      const user: User = this.loginForm.value as User;
      this.authService.login(user).subscribe({
        next: () => {
          this.loginForm.reset();
          this.loading = false;
          this.showToast('Login Successful!', 'success');
          this.router.navigate(['home'])
        },  
        error: () => {
          this.showToast('Login Failed. Try again!', 'error');
          this.loading = false;
        }
      })
    } else {
      this.showToast('Form is invalid!', 'error');
    }
    
  } 

}
