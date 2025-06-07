import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-pago',
  imports: [],
  templateUrl: './pago.component.html',
  styleUrl: './pago.component.css'
})
export class PagoComponent {
  constructor(private router: Router) {}

  ngOnInit(): void {
    const navigationState = history.state;

    setTimeout(() => {
      this.router.navigate(['/perfil'], {
        state: { membresiaActivada: navigationState?.membresiaActivada }
      });
    }, 3000);
  }
}
