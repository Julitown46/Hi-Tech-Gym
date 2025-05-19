import { Component } from '@angular/core';
import { RouterLink, Router, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { LoginService } from '../../services/login.service';
import { ToastService } from '../../services/toast.service';

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, CommonModule],
  standalone: true,
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {

  logoutMessage = '';

  constructor(public loginService: LoginService, private router: Router, private toastService: ToastService) { }

  ngOnInit() {
    this.loginService.syncLoginStatus();
  }

  async cerrarSesion() {
    try {
      await this.loginService.logout();
      this.logoutMessage = 'Sesión cerrada correctamente';
      this.toastService.showMessage('Sesion cerrada correctamente');
      this.router.navigate(['/']);
    } catch (error) {
      this.logoutMessage = 'Error al cerrar sesión';
      console.error(error);
    }
  }

}
