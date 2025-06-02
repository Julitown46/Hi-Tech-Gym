import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { Reserva } from '../../models/Reserva';
import { Pista } from '../../models/Pista';
import { ReservaFormData } from '../../models/ReservaFormData';
import { ReservaService } from '../../services/reserva.service';
import { CsrfService } from '../../services/csrf.service';
import { ToastService } from '../../services/toast.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DatePipe } from '@angular/common';

@Component({
  selector: 'app-reservas',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './reservas.component.html',
  styleUrls: ['./reservas.component.css']
})
export class ReservasComponent implements OnInit {
  reservas: Reserva[] = [];
  pistas: Pista[] = [];

  nuevaReserva: ReservaFormData = {
    pista: null,
    fecha: '',
    hora: ''
  };

  constructor(
    private reservaService: ReservaService,
    private csrfService: CsrfService,
    private toastService: ToastService,
    private http: HttpClient
  ) { }

  ngOnInit(): void {
    this.cargarReservas();
    this.cargarPistas();
  }

  cargarReservas(): void {
    this.reservaService.getReservasDelUsuarioActual().subscribe({
      next: (res) => this.reservas = res,
      error: (err) => {
        console.error('Error al cargar reservas', err);
        this.toastService.showMessage('Error al cargar reservas');
      }
    });
  }

  cargarPistas(): void {
    this.http.get<Pista[]>('http://localhost:8000/pistas/', { withCredentials: true }).subscribe({
      next: (res) => this.pistas = res.filter(p => p.activa),
      error: (err) => {
        console.error('Error al cargar pistas', err);
        this.toastService.showMessage('Error al cargar pistas');
      }
    });
  }

  async crearReserva(): Promise<void> {
    if (
      this.nuevaReserva.pista === null ||
      !this.nuevaReserva.fecha ||
      !this.nuevaReserva.hora
    ) {
      this.toastService.showMessage('Todos los campos son obligatorios');
      return;
    }

    try {
      const csrfToken = await this.csrfService.getCsrfToken();

      const headers = new HttpHeaders({
        'X-CSRFToken': csrfToken
      });
console.log('Reserva a enviar:', this.nuevaReserva);
      const nueva = await firstValueFrom(
        this.http.post<Reserva>(
          'http://localhost:8000/reservas/',
          this.nuevaReserva,
          {
            headers,
            withCredentials: true
          }
        )
      );

      this.reservas.push(nueva);
      this.toastService.showMessage('Reserva creada correctamente');
      this.nuevaReserva = { pista: 0, fecha: '', hora: '' };

    } catch (error: any) {
      console.error('Error al crear reserva', error);
      if (error.error && typeof error.error === 'object') {
        const errores = Object.entries(error.error).map(([campo, mensajes]) =>
          `${(mensajes as string[]).join(', ')}`
        );
        this.toastService.showMessage(errores.join(' | '));
      } else {
        this.toastService.showMessage('No se pudo crear la reserva');
      }
    }
  }
}
