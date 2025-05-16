import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LogoutService {

  constructor(private http: HttpClient) {}

  async logout() {
    await firstValueFrom(this.http.post('http://localhost:8000/logout/', {}, { withCredentials: true }));
    localStorage.removeItem('isLoggedIn');
  }
}
