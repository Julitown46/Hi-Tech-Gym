import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { firstValueFrom } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CsrfService {

  constructor(private http: HttpClient) { }

  async getCsrfToken(): Promise<string> {
    const response: any = await firstValueFrom(
      this.http.get('http://localhost:8000/csrf/', { withCredentials: true })
    );
    return response.csrfToken;
  }
}
