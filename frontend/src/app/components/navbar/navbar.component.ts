import { Component } from '@angular/core';
import { RouterLink, Router, RouterModule } from '@angular/router'; 
import { CommonModule } from '@angular/common';
import { LoginService } from '../../services/login.service';
import { LogoutService } from '../../services/logout.service';

@Component({
  selector: 'app-navbar',
  imports: [RouterLink, CommonModule],
  standalone: true,
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})
export class NavbarComponent {

  logoutMessage = '';

    constructor(public loginService: LoginService, private router: Router, public logoutService: LogoutService) {}

      ngOnInit() {
      this.loginService.syncLoginStatus();
    }

  async logout() {
    try {
      await this.logoutService.logout();
      this.loginService.logout();
      this.logoutMessage = 'Has cerrado sesión correctamente. Redirigiendo al inicio...';
      setTimeout(() => {
        this.logoutMessage = '';
        this.router.navigate(['/']);
      }, 2000);
    } catch (error) {
      console.error('Error al cerrar sesión en el servidor', error);
    }
  }
}
