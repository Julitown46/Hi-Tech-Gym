import { Component } from '@angular/core';
import { LoginService } from '../../services/login.service';

@Component({
  selector: 'app-reservas',
  imports: [],
  templateUrl: './reservas.component.html',
  styleUrl: './reservas.component.css'
})
export class ReservasComponent {

  constructor(private loginService: LoginService) {}

  get isLoggedIn(): boolean {
    return this.loginService.isLoggedIn();
  }

}
