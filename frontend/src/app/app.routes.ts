import { Routes } from '@angular/router';
import { InicioComponent } from './components/inicio/inicio.component';
import { PerfilComponent } from './components/perfil/perfil.component';
import { ContactoComponent } from './components/contacto/contacto.component';
import { ReservasComponent } from './components/reservas/reservas.component';
import { RegisterComponent } from './components/register/register.component';
import { PagoComponent } from './components/pago/pago.component';
import { LoginComponent } from './components/login/login.component';
import { authGuard } from './services/auth.guard';

export const routes: Routes = [
    { path: '', component: InicioComponent },
    { path: 'login', component: LoginComponent },
    { path: 'perfil', component: PerfilComponent, canActivate: [authGuard] },
    { path: 'sobre-nosotros', component: ContactoComponent },
    { path: 'reservas', component: ReservasComponent, canActivate: [authGuard] },
    { path: 'register', component: RegisterComponent },
    { path: 'pago', component: PagoComponent },
    { path: '**', redirectTo: 'login' }
];
