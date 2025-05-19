import { Component } from '@angular/core';
import { LoginService } from '../../services/login.service';

@Component({
  selector: 'app-register',
  imports: [],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {

  constructor(private loginService: LoginService) {}

  get isLoggedIn(): boolean {
    return this.loginService.isLoggedIn();
  }

  register() {
    console.log('User registered');
  }

}
