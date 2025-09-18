import { Routes } from '@angular/router';
import { Signup } from '../pages/signup/signup';
import { Login } from '../pages/login/login';
import { Home } from '../pages/home/home'; 
import { Otp } from '../pages/otp/otp';

export const routes: Routes = [
  { path: '', redirectTo: 'signup', pathMatch: 'full' }, // default → signup
  { path: 'signup', component: Signup },
  { path: 'login', component: Login },
  { path: 'verify-otp', component: Otp },
  { path: 'home', component: Home },
  { path: '**', redirectTo: 'signup' }
];
