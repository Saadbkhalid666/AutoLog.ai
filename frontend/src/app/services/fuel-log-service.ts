import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface FuelLog {
  id?: number;
  user_id?: number;
  date: string;
  litres: string;
  price: string;
  odometer: string;
}

@Injectable({
  providedIn: 'root'
})
export class FuelLogService {
  private baseUrl = 'http://127.0.0.1:5000/vehicle';

  constructor(private http: HttpClient) {}

  private getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
      headers: new HttpHeaders({
        Authorization: token ? `Bearer ${token}` : ''
      })
    };
  }

  getFuelLogs(): Observable<any> {
    return this.http.get(`${this.baseUrl}/get-fuel-logs`, this.getAuthHeaders());
  }

  addManualFuelLog(log: FuelLog): Observable<any> {
    return this.http.post(`${this.baseUrl}/fuel-log/manual`, log, this.getAuthHeaders());
  }

  uploadOCRFuelLog(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.baseUrl}/fuel-logs/ocr`, formData, this.getAuthHeaders());
  }

  deleteFuelLog(logId: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/delete-fuel-log/${logId}`, this.getAuthHeaders());
  }

  updateFuelLog(logId: number, log: FuelLog): Observable<any> {
    return this.http.put(`${this.baseUrl}/update-fuel-log/${logId}`, log, this.getAuthHeaders());
  }
}
