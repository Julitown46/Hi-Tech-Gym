import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class RegisterService {

  private apiUrl = 'http://localhost:8000/usuarios/';

  constructor(private http: HttpClient) { }

  register(userData: { username: string; email: string; password: string }) {
    return this.http.post(this.apiUrl, userData, { withCredentials: true });
  }
}
