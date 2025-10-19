import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface FuelLog {
  id?: number;
  user_id?: number;
  date: string;
  litres?: number;
  price?: number;
  odometer?: number;
  created_at?: string;
}

@Injectable({
  providedIn: 'root'
})
export class FuelLogService {
  private baseUrl = 'https://autolog-backend-ecc53876d2e8.herokuapp.com/vehicle';

  constructor(private http: HttpClient) {}

  private getAuthHeaders() {
    const token = localStorage.getItem('token') || '';
    return {
      headers: new HttpHeaders({
        Authorization: token ? `Bearer ${token}` : '',
         'Content-Type': 'application/json' 
      })
    };
  }

  getFuelLogs(): Observable<{ fuel_logs: FuelLog[] }> {
    return this.http.get<{ fuel_logs: FuelLog[] }>(`${this.baseUrl}/get-fuel-logs`, this.getAuthHeaders());
  }

  addManualFuelLog(log: Partial<FuelLog>): Observable<any> {
    return this.http.post(`${this.baseUrl}/fuel-log/manual`, log, this.getAuthHeaders());
  }

  updateFuelLog(logId: number, log: Partial<FuelLog>): Observable<any> {
    return this.http.put(`${this.baseUrl}/update-fuel-log/${logId}`, log, this.getAuthHeaders());
  }

  deleteFuelLog(logId: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/delete-fuel-log/${logId}`, this.getAuthHeaders());
  }
}
