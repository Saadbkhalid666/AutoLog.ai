import { HttpClient } from '@angular/common/http';
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
  private apiUrl = 'http://localhost:5000/auth';
  private usernameSubject = new BehaviorSubject<string | null>(null);
  username$ = this.usernameSubject.asObservable();

  constructor(private http: HttpClient) {
    const savedUsername = sessionStorage.getItem('username');
    if (savedUsername) {
      this.usernameSubject.next(savedUsername);
    }
  }

  signup(user: User): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/register`, user, {withCredentials:true}).pipe(
      tap((res) => {
        if (res?.username) {
          sessionStorage.setItem('username', res.username);
          this.usernameSubject.next(res.username);
        }
      })
    );
  }

  login(credentials: { email: string; password: string }): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/login`, credentials, { withCredentials: true }).pipe(
      tap((res) => {
        if (res?.username) {
          sessionStorage.setItem('username', res.username);
          this.usernameSubject.next(res.username);

        }
      })
    );
  }

  verifyOtp(otpData: { otp: string }): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/verify-otp`, otpData, {withCredentials:true}).pipe(
      tap((res) => {
        if (res?.username) {
          localStorage.setItem('username', res.username);
          this.usernameSubject.next(res.username);
        }
      })
    );
  }

  getUsername(): string | null {
    return this.usernameSubject.value;
  }

  checkUserName(): string | null {
    return this.usernameSubject.value;
  }

  logout(): void {
    localStorage.removeItem('username');
    this.usernameSubject.next(null);
  }
}
