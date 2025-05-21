import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Membresia } from '../models/Membresia';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MembresiaService {
  private apiUrl = 'http://localhost:8000/membresias/';

  constructor(private http: HttpClient) {}

  getMembresias(): Observable<Membresia[]> {
    return this.http.get<Membresia[]>(this.apiUrl);
  }

  getMembresiasPorUsuario(usuarioId: number): Observable<Membresia[]> {
    return this.http.get<Membresia[]>(`${this.apiUrl}?usuario=${usuarioId}`);
  }
}
