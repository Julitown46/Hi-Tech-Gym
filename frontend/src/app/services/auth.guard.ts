import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { LoginService } from './login.service';
import { ToastService } from './toast.service';

export const authGuard: CanActivateFn = (route, state) => {
  const loginService = inject(LoginService);
  const router = inject(Router);
  const toastService = inject(ToastService);

  const usuario = loginService.getUsuarioLogueado();

  if (!usuario) {
    toastService.showMessage('Debes iniciar sesión para acceder.');
    router.navigate(['/login']);
    return false;
  }

  // 👇 Solo requerir membresía si la ruta es `/reservas`
  if (state.url.startsWith('/reservas') && !usuario.membresia_activa) {
    toastService.showMessage('Necesitas una membresía activa para acceder a esta sección.');
    router.navigate(['/perfil']);
    return false;
  }

  return true;
};