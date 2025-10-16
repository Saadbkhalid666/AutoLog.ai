import { Routes } from '@angular/router';
import { Signup } from './pages/signup/signup';
import { Login } from './pages/login/login';
import { Otp } from './pages/otp/otp';
import { Home } from './pages/home/home';
import { Terms } from './pages/terms/terms';
import { Policy } from './pages/policy/policy';
import {  FuelLogs } from './pages/fuel-log/fuel-log';
import { Reminder } from './pages/reminder/reminder';
import { OcrComponent } from './pages/ocr/ocr';
import { AuthGuard } from './guard/auth.guard';
import { AiChatComponent } from './pages/assistant/assistant';
import { AdminComponent } from './pages/admin/admin';
import { AccessFormComponent } from './pages/access-form/access-form';

export const routes: Routes = [
   { path: '', component: Home, canActivate: [AuthGuard] },
  { path: 'signup', component: Signup },
  { path: 'login', component: Login },
  { path: 'verify-otp', component: Otp },
  { path: 'home', component: Home },
  { path: 'terms', component: Terms },
  {path:'privacy', component: Policy},
  {path:'fuellog/mannual',component:FuelLogs},
  {path:'service-reminders', component:Reminder},
  {path:'fuellog/ocr', component:OcrComponent},
  {path:'assistant/c', component:AiChatComponent},
  {path:'admin', component:AdminComponent},
  {path:'db-access-form', component:AccessFormComponent},
  { path: '**', redirectTo: 'signup' },
];
