import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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
  private baseUrl = 'http://localhost:5000/vehicle'; // Flask API URL
  constructor(private http: HttpClient) {}

  getFuelLogs(): Observable<any> {
  const token = localStorage.getItem('token');

    return this.http.get(`${this.baseUrl}/get-fuel-logs`, { withCredentials: true });

  }

  addManualFuelLog(log: FuelLog): Observable<any> {
    return this.http.post(`${this.baseUrl}/fuel-log/manual`, log, { withCredentials: true });
  }

  uploadOCRFuelLog(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.baseUrl}/fuel-logs/ocr`, formData, { withCredentials: true });
  }

  deleteFuelLog(logId: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/delete-fuel-log/${logId}`, { withCredentials: true });
  }

  updateFuelLog(logId: number, log: FuelLog): Observable<any> {
    return this.http.put(`${this.baseUrl}/update-fuel-log/${logId}`, log, { withCredentials: true });
  }
}
