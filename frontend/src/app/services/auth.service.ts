import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap } from 'rxjs';

export interface User {
  username: string;
  email: string;
  password: string;
}

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = 'https://autolog-backend-7961ac6afab3.herokuapp.com/auth';
  private usernameSubject = new BehaviorSubject<string | null>(null);
  username$ = this.usernameSubject.asObservable();
  private userRoleSubject = new BehaviorSubject<string | null>(localStorage.getItem('role'));
  userRole$ = this.userRoleSubject.asObservable();

  constructor(private http: HttpClient) {
    const savedUsername = localStorage.getItem('username');
    if (savedUsername) {
      this.usernameSubject.next(savedUsername);
    }
  }

  signup(user: User): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/register`, user).pipe(
      tap((res) => {
        if (res?.token && res?.username) {
          localStorage.setItem('token', res.token);
          localStorage.setItem('username', res.username);
          this.usernameSubject.next(res.username);
        }
      })
    );
  }

  verifyOtp(otpData: { otp: string }): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/verify-otp`, otpData).pipe(
      tap((res) => {
        if (res?.token && res?.username) {
          localStorage.setItem('token', res.token);
          localStorage.setItem('username', res.username);
          localStorage.setItem('role', res.role);

          this.usernameSubject.next(res.username);
          this.userRoleSubject.next(res.role)
        }
      })
    );
  }

  login(credentials: { email: string; password: string }): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/login`, credentials).pipe(
      tap((res) => {
        if (res?.token && res?.username) {
          localStorage.setItem('token', res.token);
          localStorage.setItem('username', res.username);
          localStorage.setItem('role', res.role);
          this.usernameSubject.next(res.username);

           this.userRoleSubject.next(res.role);
        }
      })
    );
  }

  getUsername(): string | null {
    return this.usernameSubject.value;
  }
  

  getToken(): string | null {
    return localStorage.getItem('token');
  }

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    this.usernameSubject.next(null);
  }

  getAuthHeaders(): { headers: HttpHeaders } {
    const token = this.getToken();
    return {
      headers: new HttpHeaders({
        Authorization: token ? `Bearer ${token}` : '',
      }),
    };
  }
  

}
