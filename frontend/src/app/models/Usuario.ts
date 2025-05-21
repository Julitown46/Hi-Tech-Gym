export interface Usuario {
  id: number;
  username: string;
  email: string;
  membresia_activa: boolean;
  rol: 'superuser' | 'admin' | 'usuario';
}