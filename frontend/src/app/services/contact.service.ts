// src/app/services/contact.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ContactPayload {
  name: string;
  email: string;
  message: string;
}

@Injectable({
  providedIn: 'root'
})
export class ContactService {
  private baseUrl = 'http://127.0.0.1:5000'; 

  constructor(private http: HttpClient) {}

  submitContact(payload: ContactPayload): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/form/contact`, payload);
  }
}
