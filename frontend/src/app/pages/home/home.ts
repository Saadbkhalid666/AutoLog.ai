import { CommonModule } from '@angular/common';
import { Component,  } from '@angular/core';
import { Services } from '../../sections/services/services';
import { Hero } from '../../sections/hero/hero';
import { About } from '../../sections/about/about';
import { CarModel } from '../../components/car-model/car-model';
import { ContactComponent } from '../../sections/contact/contact';

@Component({
  selector: 'app-home',
  imports:[CommonModule,Services, Hero, About, CarModel, ContactComponent ],
  templateUrl: './home.html',
  styleUrls: ['./home.css']
})
export class Home  {
}
