import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Pista } from '../models/Pista';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PistaService {
  private apiUrl = 'http://localhost:8000/pistas/';

  constructor(private http: HttpClient) {}

  getPistas(): Observable<Pista[]> {
    return this.http.get<Pista[]>(this.apiUrl);
  }

  getPista(id: number): Observable<Pista> {
    return this.http.get<Pista>(`${this.apiUrl}${id}/`);
  }
}
