import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Otp } from '../pages/otp/otp';
import { Signup } from '../pages/signup/signup';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,Otp,Signup],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}
