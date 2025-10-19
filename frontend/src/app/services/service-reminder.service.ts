import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ServiceReminder {
  id?: number;
  service_type: string;
  due_date: string;
  note: string;
  status?: string;
  created_at?: string;
}
@Injectable({ providedIn: 'root' })
export class ServiceReminderService {
  private baseUrl = 'https://autolog-backend-ecc53876d2e8.herokuapp.com/service-reminders';

  constructor(private http: HttpClient) {}

  private getAuthHeaders() {
    return {
      headers: new HttpHeaders({
        Authorization: `Bearer ${localStorage.getItem('token')}`
      })
    };
  }

  getReminders(): Observable<ServiceReminder[]> {
    return this.http.get<ServiceReminder[]>(`${this.baseUrl}/get`, this.getAuthHeaders());
  }

  addReminder(reminder: ServiceReminder) {
    return this.http.post(`${this.baseUrl}/add`, reminder, this.getAuthHeaders());
  }

  updateReminder(id: number, reminder: ServiceReminder) {
    return this.http.put(`${this.baseUrl}/update/${id}`, reminder, this.getAuthHeaders());
  }

  deleteReminder(id: number) {
    return this.http.delete(`${this.baseUrl}/delete/${id}`, this.getAuthHeaders());
  }
}
