import { Component } from '@angular/core';
import { CarModel } from '../../components/car-model/car-model';

@Component({
  selector: 'app-about',
  standalone:true,
  imports: [CarModel],
  templateUrl: './about.html',
  styleUrl: './about.css'
})
export class About {

}
 