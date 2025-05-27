import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Reserva } from '../models/Reserva';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ReservaService {
  private apiUrl = 'http://localhost:8000/reservas/';

  constructor(private http: HttpClient) {}

  getReservas(): Observable<Reserva[]> {
    return this.http.get<Reserva[]>(this.apiUrl, { withCredentials: true });
  }

  getReservasPorUsuario(usuarioId: number): Observable<Reserva[]> {
    return this.http.get<Reserva[]>(`${this.apiUrl}?usuario=${usuarioId}`, {
      withCredentials: true
    });
  }

  createReserva(reserva: Reserva): Observable<Reserva> {
    return this.http.post<Reserva>(this.apiUrl, reserva, {
      withCredentials: true
    });
  }

  cancelarReserva(id: number): Observable<any> {
    return this.http.patch(`${this.apiUrl}${id}/`, { estado: 'cancelada' }, {
      withCredentials: true
    });
  }

  getReservasDelUsuarioActual(): Observable<Reserva[]> {
  return this.http.get<Reserva[]>('http://localhost:8000/reservas/mis-reservas/', {
    withCredentials: true
  });
}

}
