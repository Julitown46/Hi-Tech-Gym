import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Usuario } from '../../models/Usuario';
import { Reserva } from '../../models/Reserva';
import { ReservaService } from '../../services/reserva.service';
import { LoginService } from '../../services/login.service';
import { catchError } from 'rxjs/operators';
import { firstValueFrom, of } from 'rxjs';
import { ToastService } from '../../services/toast.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { MembresiaService } from '../../services/membresia.service';


@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './perfil.component.html'
})
export class PerfilComponent implements OnInit {
  private reservaService = inject(ReservaService);
  private loginService = inject(LoginService);
  private toastService = inject(ToastService);
  private http = inject(HttpClient);
  private membresiaService = inject(MembresiaService);


  usuario: Usuario | null = null;
  reservas: Reserva[] = [];
  error: string | null = null;

  ngOnInit(): void {
    const usuario = this.loginService.getUsuarioLogueado();
    console.log('Usuario cargado desde LoginService:', usuario);

    if (!usuario) {
      this.error = 'No se encontró información del usuario.';
      return;
    }

    this.usuario = usuario;

    this.reservaService.getReservasDelUsuarioActual().subscribe(reservas => {
      this.reservas = reservas;
    });
  }


  cargarPerfil(): void {
    const usuario = this.loginService.getUsuarioLogueado();

    if (!usuario) {
      this.error = 'No se encontró información del usuario.';
      return;
    }

    this.usuario = usuario;

    this.reservaService.getReservasPorUsuario(usuario.id).pipe(
      catchError(err => {
        console.error('Error al obtener reservas:', err);
        this.error = 'No se pudieron cargar las reservas.';
        return of([]);
      })
    ).subscribe(reservas => {
      this.reservas = reservas.filter(r => r.estado === 'confirmada');
    });
  }

  async activarMembresia(): Promise<void> {
    if (!this.usuario) {
      this.toastService.showMessage('No se puede activar membresía sin usuario.');
      return;
    }

    try {
      const csrfResponse: any = await firstValueFrom(
        this.http.get('http://localhost:8000/csrf/', { withCredentials: true })
      );

      const csrfToken = csrfResponse.csrfToken;

      const headers = new HttpHeaders({
        'X-CSRFToken': csrfToken
      });

      const response = await firstValueFrom(
        this.http.post('http://localhost:8000/membresias/', {}, {
          headers,
          withCredentials: true
        })
      );

      this.toastService.showMessage('¡Membresía activada correctamente!');
      const actualizado = { ...this.usuario!, membresia_activa: true };
      this.loginService.setUsuarioLogueado(actualizado);
      this.usuario = actualizado;

    } catch (err) {
      console.error('Error al activar membresía:', err);
      this.toastService.showMessage('No se pudo activar la membresía.');
    }
  }

}
