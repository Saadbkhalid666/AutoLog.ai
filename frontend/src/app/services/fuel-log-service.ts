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

  getFuelLogs(userId: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/get-fuel-logs/${userId}`);
  }

  addManualFuelLog(log: FuelLog): Observable<any> {
    return this.http.post(`${this.baseUrl}/fuel-log/manual`, log);
  }

  uploadOCRFuelLog(file: File): Observable<any> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post(`${this.baseUrl}/fuel-logs/ocr`, formData);
  }

  deleteFuelLog(logId: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/delete-fuel-log/${logId}`);
  }

  updateFuelLog(logId: number, log: FuelLog): Observable<any> {
    return this.http.put(`${this.baseUrl}/update-fuel-log/${logId}`, log);
  }
}
