import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { ToastService } from '../../services/toast.service';
import { LoginService } from '../../services/login.service';

@Component({
  selector: 'app-login',
  imports: [CommonModule, ReactiveFormsModule, HttpClientModule, RouterModule],
  standalone: true,
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  loginForm: FormGroup;
  errorMessage: string | null = null;

  constructor(private fb: FormBuilder, private toastService: ToastService, private http: HttpClient, private router: Router, public loginService: LoginService) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      this.loginService.login(this.loginForm.value)
        .then(response => {
          console.log('Login exitoso:', response);
          console.log('Usuario guardado:', this.loginService.getUsuarioLogueado());
          this.toastService.showMessage('Sesión iniciada correctamente');
          this.router.navigate(['/']);
        })
        .catch(error => {
          console.error('Error al iniciar sesión', error);
          this.errorMessage = 'Credenciales incorrectas o usuario no válido';
        });
    } else {
      this.toastService.showMessage('Por favor, rellene todos los datos');
    }
  }

}
