import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ServiceReminder {
  id?: number;
  user_id: number;
  service_type: string;
  due_date: string;
  note: string;
  status?: string;
  created_at?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ServiceReminderService {
  private baseUrl = 'http://127.0.0.1:5000/service-reminders'; // change if needed

  constructor(private http: HttpClient) {}

  getReminders(user_id: number): Observable<ServiceReminder[]> {
    return this.http.get<ServiceReminder[]>(`${this.baseUrl}/get/${user_id}`);
  }

  addReminder(reminder: ServiceReminder): Observable<any> {
    return this.http.post(`${this.baseUrl}/add`, reminder);
  }

  updateReminder(id: number, reminder: ServiceReminder): Observable<any> {
    return this.http.put(`${this.baseUrl}/update/${id}`, reminder);
  }

  deleteReminder(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/delete/${id}`);
  }
}
