import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap } from 'rxjs';

export interface FuelLog{
     id?: number;
  user_id?: number;
  date: string;
  litres: number;
  price: number;
  odometer: number;
  created_at?: string;
}
 
@Injectable({
  providedIn: 'root',
})

export class OCRService {
    private baseUrl = 'http://127.0.0.1:500/vehicle';

    constructor(private http:HttpClient){}

    private getAuthHeaders(){
        const token = localStorage.getItem('token') || '';
        return {
            headers: new HttpHeaders({
                Authorization: token ? `Bearer ${token}`
            })
        }
    }
    
     
      }
    
}