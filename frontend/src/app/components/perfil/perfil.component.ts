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
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { Location } from '@angular/common';


@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [CommonModule, FormsModule],
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

  constructor(
    private router: Router,
    private location: Location,
  ) { }

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

    const state = this.location.getState() as { membresiaActivada?: boolean };

    if (state?.membresiaActivada) {
      this.toastService.showMessage('¡Membresía activada correctamente!');
    }
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
      this.reservas = reservas;
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

      const actualizado = { ...this.usuario!, membresia_activa: true };
      this.loginService.setUsuarioLogueado(actualizado);
      this.usuario = actualizado;
      this.router.navigate(['/pago'], {
        state: { membresiaActivada: true }
      });
    } catch (err) {
      console.error('Error al activar membresía:', err);
      this.toastService.showMessage('No se pudo activar la membresía.');
    }
  }

  mostrarConfirmacion = false;

  confirmarCancelacion(): void {
    this.mostrarConfirmacion = true;
  }

  async cancelarMembresia(): Promise<void> {
    this.mostrarConfirmacion = false;

    if (!this.usuario) {
      this.toastService.showMessage('No se puede cancelar sin usuario.');
      return;
    }

    try {
      const csrfToken = await this.loginService['getCsrfToken']();

      const headers = new HttpHeaders({
        'X-CSRFToken': csrfToken
      });

      await firstValueFrom(
        this.http.delete('http://localhost:8000/membresias/cancelar/', {
          headers,
          withCredentials: true
        })
      );

      const actualizado = { ...this.usuario, membresia_activa: false };
      this.loginService.setUsuarioLogueado(actualizado);
      this.usuario = actualizado;

      this.toastService.showMessage('Membresía cancelada con éxito.');
    } catch (error) {
      console.error('Error al cancelar la membresía:', error);
      this.toastService.showMessage('Error al cancelar la membresía.');
    }
  }

  filtroEstado: string = 'todas';

  get reservasFiltradas() {
    if (this.filtroEstado === 'todas') {
      return this.reservas;
    }
    return this.reservas.filter(r => r.estado === this.filtroEstado);
  }
}
