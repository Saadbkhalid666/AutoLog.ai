import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Nav } from './components/nav/nav';
import { Footer } from './sections/footer/footer';

@Component({
  selector: 'app-root',
  standalone: true, 
  imports: [RouterOutlet,Nav,Footer],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}
 