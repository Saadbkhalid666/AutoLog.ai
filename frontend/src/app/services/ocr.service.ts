import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class OcrFuelService {
  private baseUrl = 'https://autolog-backend-7961ac6afab3.herokuapp.com/vehicle';
  private tokenKey = 'token';

  constructor(private http: HttpClient) {}

  private getAuthHeaders(): HttpHeaders {
    const token = localStorage.getItem(this.tokenKey);
    return new HttpHeaders({
      Authorization: token ? `Bearer ${token}` : ''
    });
  }

  getFuelLogs(): Observable<any> {
    return this.http.get(`${this.baseUrl}/get-fuel-logs`, {
      headers: this.getAuthHeaders()
    });
  }

  uploadOcr(file: File): Observable<any> {
    const form = new FormData();
    form.append('file', file);

    return this.http.post(`${this.baseUrl}/fuel-logs/ocr`, form, {
      headers: this.getAuthHeaders()
    });
  }
}
