import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private readonly baseUrl = 'http://127.0.0.1:5000/admin_auth';

  constructor(private http: HttpClient) {}

  adminLogin(credentials: { email: string; password: string }): Observable<any> {
    const headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    return this.http.post(`${this.baseUrl}/login`, credentials, {
      headers,
      withCredentials: true // for Flask session cookie
    });
  }

  checkAuth(): Observable<any> {
    return this.http.get(`${this.baseUrl}/debug-auth`, {
      withCredentials: true
    });
  }

  logout(): Observable<any> {
    return this.http.get(`${this.baseUrl}/logout`, {
      withCredentials: true
    });
  }
}
