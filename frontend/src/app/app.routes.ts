import { Routes } from '@angular/router';
import { Login } from '../pages/login/login';
import { Signup } from '../pages/signup/signup';
import { Otp } from '../pages/otp/otp';
import { App } from './app';

export const routes: Routes = [
    {path:'/',component:App},
    {path:'/login', component:Login},
    {path:'/signup', component:Signup},
    {path:'/verify-otp', component:Otp}
];
