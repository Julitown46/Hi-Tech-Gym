import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Usuario } from '../../models/Usuario';
import { Reserva } from '../../models/Reserva';
import { ReservaService } from '../../services/reserva.service';
import { LoginService } from '../../services/login.service';
import { catchError } from 'rxjs/operators';
import { of } from 'rxjs';

@Component({
  selector: 'app-perfil',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './perfil.component.html'
})
export class PerfilComponent implements OnInit {
  private reservaService = inject(ReservaService);
  private loginService = inject(LoginService);

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

    this.reservaService.getReservasPorUsuario(usuario.id).subscribe(reservas => {
      this.reservas = reservas.filter(r => r.estado === 'confirmada');
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
}
