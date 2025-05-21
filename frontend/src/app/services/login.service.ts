import { Injectable } from '@angular/core';
import { BehaviorSubject, firstValueFrom } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Usuario } from '../models/Usuario';
import { ToastService } from './toast.service';

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  private readonly STORAGE_KEY = 'isLoggedIn';
  private loggedInSubject = new BehaviorSubject<boolean>(this.getStoredStatus());
  private usuario: Usuario | null = null;

  setUsuarioLogueado(usuario: Usuario) {
    this.usuario = usuario;
  }

  getUsuarioLogueado(): Usuario | null {
    return this.usuario;
  }

  loggedIn$ = this.loggedInSubject.asObservable();

  constructor(private http: HttpClient, private toastService: ToastService) { }

  private isBrowser(): boolean {
    return typeof window !== 'undefined' && typeof localStorage !== 'undefined';
  }

  private getStoredStatus(): boolean {
    if (this.isBrowser()) {
      return localStorage.getItem(this.STORAGE_KEY) === 'true';
    }
    return false;
  }

  private async getCsrfToken(): Promise<string> {
    const response: any = await firstValueFrom(
      this.http.get('http://localhost:8000/csrf/', { withCredentials: true })
    );
    return response.csrfToken;
  }

  async login(credentials: any): Promise<any> {
    const csrfToken = await this.getCsrfToken();

    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken
    });

    try {
      const response: any = await firstValueFrom(
        this.http.post('http://localhost:8000/login/', credentials, {
          headers,
          withCredentials: true
        })
      );

      if (this.isBrowser()) {
        localStorage.setItem(this.STORAGE_KEY, 'true');
        this.loggedInSubject.next(true);
      }

      this.setUsuarioLogueado(response);

      return response;

    } catch (error) {
      this.toastService.showMessage('Error al iniciar sesion');
      console.error('Error al iniciar sesión:', error);
      throw error;
    }
  }

  async logout(): Promise<any> {
    const csrfToken = await this.getCsrfToken();

    const headers = new HttpHeaders({
      'X-CSRFToken': csrfToken
    });

    try {
      const response = await firstValueFrom(
        this.http.post('http://localhost:8000/logout/', {}, {
          headers,
          withCredentials: true
        })
      );

      this.clearLoginStatus();
      return response;

    } catch (error) {
      this.toastService.showMessage('Error al cerrar sesion');
      console.error('Error al cerrar sesión:', error);
      this.clearLoginStatus();
      throw error;
    }
  }

  private clearLoginStatus() {
    if (this.isBrowser()) {
      localStorage.removeItem(this.STORAGE_KEY);
      this.loggedInSubject.next(false);
    }
  }

  isLoggedIn(): boolean {
    return this.loggedInSubject.value;
  }

  syncLoginStatus() {
    this.loggedInSubject.next(this.getStoredStatus());
  }
}
