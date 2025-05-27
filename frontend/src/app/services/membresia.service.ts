import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Membresia } from '../models/Membresia';
import { Observable, firstValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MembresiaService {
  private apiUrl = 'http://localhost:8000/membresias/';

  constructor(private http: HttpClient) {}

  getMembresias(): Observable<Membresia[]> {
    return this.http.get<Membresia[]>(this.apiUrl, { withCredentials: true });
  }

  getMembresiasPorUsuario(usuarioId: number): Observable<Membresia[]> {
    return this.http.get<Membresia[]>(`${this.apiUrl}?usuario=${usuarioId}`, {
      withCredentials: true
    });
  }

  async getCsrfToken(): Promise<string> {
    const response: any = await firstValueFrom(
      this.http.get('http://localhost:8000/csrf/', { withCredentials: true })
    );
    return response.csrfToken;
  }

  async activarMembresia(): Promise<Membresia> {
    const csrfToken = await this.getCsrfToken();
    const headers = new HttpHeaders({ 'X-CSRFToken': csrfToken });

    const response = await firstValueFrom(
      this.http.post<Membresia>(this.apiUrl, {}, {
        headers,
        withCredentials: true
      })
    );

    return response;
  }
}
