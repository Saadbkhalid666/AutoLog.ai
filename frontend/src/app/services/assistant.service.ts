import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  reply: string;
}

@Injectable({
  providedIn: 'root'
})
export class AiService {
  private baseUrl = ' http://127.0.0.1:5000/chat' ;

  constructor(private http: HttpClient) {}

  private headers(): HttpHeaders {
    // If you use a token, swap here. Example: localStorage.getItem('token')
    const token = localStorage.getItem('token');
    return new HttpHeaders({
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {})
    });
  }

  chat(req: ChatRequest): Observable<ChatResponse> {
    return this.http.post<ChatResponse>(`${this.baseUrl}/c`, req, { headers: this.headers() });
  }
}
