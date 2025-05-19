import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { LoginService } from '../../services/login.service';
import { CommonModule } from '@angular/common';
import { ToastService } from '../../services/toast.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  standalone: true,
  imports: [FormsModule, CommonModule],
})
export class RegisterComponent {
  errorMessage: string | null = null;
  successMessage: string | null = null;

  constructor(
    private http: HttpClient,
    private loginService: LoginService,
    private router: Router,
    private toastService: ToastService
  ) {}

  onRegister() {
    const username = (document.getElementById('username') as HTMLInputElement).value;
    const email = (document.getElementById('email') as HTMLInputElement).value;
    const password = (document.getElementById('password') as HTMLInputElement).value;
    const confirmPassword = (document.getElementById('confirmPassword') as HTMLInputElement).value;

    if (password !== confirmPassword) {
      this.errorMessage = 'Las contraseñas no coinciden';
      return;
    }

    const userData = { username, email, password };

    this.http.post('http://localhost:8000/usuarios/', userData, { withCredentials: true })
      .subscribe({
        next: () => {
          this.toastService.showMessage('Registro exitoso, sesion iniciada');
          this.autoLogin(username, password);
        },
        error: (error) => {
          console.error(error);
          this.errorMessage = 'Error al registrar el usuario.';
        }
      });
  }

  private async autoLogin(username: string, password: string) {
    try {
      await this.loginService.login({ username, password });
      this.router.navigate(['/']);
    } catch (error) {
      this.errorMessage = 'El registro fue exitoso pero no se pudo iniciar sesión automáticamente.';
    }
  }
}
