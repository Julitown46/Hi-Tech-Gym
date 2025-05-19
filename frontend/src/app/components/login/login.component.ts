import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { ToastService } from '../../services/toast.service';

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

  constructor(private fb: FormBuilder, private toastService: ToastService, private http: HttpClient, private router: Router) {
    this.loginForm = this.fb.group({
      username: ['', Validators.required],
      password: ['', Validators.required],
    });
  }

  onSubmit() {
    if (this.loginForm.valid) {
      this.http.post<any>('http://localhost:8000/login/', this.loginForm.value, { withCredentials: true })
        .subscribe({
          next: (response) => {
            console.log('Login exitoso:', response);
            this.toastService.showMessage('Sesion iniciada correctamente');
            localStorage.setItem('isLoggedIn', 'true');
            this.router.navigate(['/']);
          },
          error: (error) => {
            console.error('Error al iniciar sesión', error);
            this.errorMessage = 'Credenciales incorrectas o usuario no válido';
          }
        });
    }
  }

}
