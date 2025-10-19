import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface User {
  id: number;
  username: string;
  email: string;
  role: string;
}

export interface FuelLog {
  id: number;
  user_id: string;
  litres: number;
  price: number;
  odometer: number;
  date: string;
}

export interface Reminder {
  id: number;
  user_id: string;
  service_type: string;
  due_date: string;
  note: string;
}

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private baseUrl = 'https://autolog-backend-ecc53876d2e8.herokuapp.com/admin'; 

  constructor(private http: HttpClient) {}

  // Users
  getAllUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.baseUrl}/get-all-users`);
  }

  updateUser(id: number, data: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/update-user/${id}`, data);
  }

  deleteUser(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/del-user/${id}`);
  }

  // Fuel Logs
  getAllLogs(): Observable<FuelLog[]> {
    return this.http.get<FuelLog[]>(`${this.baseUrl}/get-all-logs`);
  }

  updateLog(id: number, data: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/update-log/${id}`, data);
  }

  deleteLog(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/del-log/${id}`);
  }

  // Service Reminders
  getAllReminders(): Observable<Reminder[]> {
    return this.http.get<Reminder[]>(`${this.baseUrl}/get-all-reminders`);
  }

  updateReminder(id: number, data: any): Observable<any> {
    return this.http.put(`${this.baseUrl}/update-reminder/${id}`, data);
  }

  deleteReminder(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/del-reminder/${id}`);
  }

  adminLogin(credentials: { email: string; password: string }): Observable<any> {
  return this.http.post<any>(`${this.baseUrl}/login`, credentials, {
    withCredentials: true // Important for session cookies
  });
}

}
