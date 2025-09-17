import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Otp } from '../pages/otp/otp';
import { Signup } from '../pages/signup/signup';
import { Login } from '../pages/login/login';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet,Otp,Signup,Login],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}
