import { CommonModule } from '@angular/common';
import { Component,  } from '@angular/core';
import { Services } from '../../sections/services/services';
import { HeroAboutCarComponent } from '../../sections/hero-about-car-component/hero-about-car-component';

@Component({
  selector: 'app-home',
  imports:[CommonModule,Services,HeroAboutCarComponent ],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class Home  {
}
