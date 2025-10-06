import { Routes } from '@angular/router';
import { Signup } from './pages/signup/signup';
import { Login } from './pages/login/login';
import { Otp } from './pages/otp/otp';
import { Home } from './pages/home/home';
import { Terms } from './pages/terms/terms';
import { Policy } from './pages/policy/policy';
import {  FuelLogs } from './pages/fuel-log/fuel-log';

export const routes: Routes = [
  { path: '', redirectTo: 'login', pathMatch: 'full' },
  { path: 'signup', component: Signup },
  { path: 'login', component: Login },
  { path: 'verify-otp', component: Otp },
  { path: 'home', component: Home },
  { path: 'terms', component: Terms },
  {path:'privacy', component: Policy},
  {path:'fuellog/mannual',component:FuelLogs},
  { path: '**', redirectTo: 'signup' },
];
