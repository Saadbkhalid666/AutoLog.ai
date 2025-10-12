import { CommonModule } from '@angular/common';
import { Component,  } from '@angular/core';
import { Services } from '../../sections/services/services';
import { Hero } from '../../sections/hero/hero';
import { About } from '../../sections/about/about';
import { CarModel } from '../../components/car-model/car-model';

@Component({
  selector: 'app-home',
  imports:[CommonModule,Services, Hero, About, CarModel ],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class Home  {
}
