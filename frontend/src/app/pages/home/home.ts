 import { Component, OnInit } from "@angular/core";
 import {AuthService} from "../../services/auth"
 import { Subscription } from 'rxjs';
 import { Router } from '@angular/router';
import { Hero } from "../../sections/hero/hero";
import { About } from "../../sections/about/about";
import { CarModel } from "../../components/car-model/car-model";
import { Features } from "../../sections/features/features";
@Component({
  selector: 'app-home',
  imports:[Hero,About,CarModel, Features],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class Home implements OnInit {
  
  constructor(private auth: AuthService, private router: Router){}

  private sub !:Subscription
  
  ngOnInit(){
    this.sub = this.auth.username$.subscribe(username =>{
      username ?  this.router.navigate(['home']) : this.router.navigate(['login'])
    })
  }

}