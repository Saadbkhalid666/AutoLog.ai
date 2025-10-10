 import { Component, OnInit } from "@angular/core";
import { Hero } from "../../sections/hero/hero";
import { About } from "../../sections/about/about";
import { CarModel } from "../../components/car-model/car-model";
import { Services } from "../../sections/services/services";
import { CommonModule } from "@angular/common";
@Component({
  selector: 'app-home',
  imports:[Hero,About,CarModel, Services, CommonModule],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home {
  

}