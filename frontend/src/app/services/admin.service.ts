import { Injectable } from '@angular/core';
import { HttpClient , HttpHeaders} from '@angular/common/http';
import { Observable } from 'rxjs';



@Injectable({
  providedIn: 'root'
})

export class Admin {
    
    private adminUrl = 'http://127.0.0.1:5000/admin_auth'
    constructor (private http: HttpClient){}
    
    adminLogin(credentials: { email: string; password: string }): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json'
    });

    return this.http.post(`${this.adminUrl}/login`, credentials, {
      headers: headers,
      withCredentials: true  // Crucial for session cookies
    });
  }

  checkAuth(): Observable<any> {
    return this.http.get(`${this.adminUrl}/debug-auth`, {
      withCredentials: true
    });
  }

  logout(): Observable<any> {
    return this.http.get(`${this.adminUrl}/logout`, {
      withCredentials: true
    });
}
}