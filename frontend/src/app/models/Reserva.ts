import { Pista } from "./Pista";

export interface Reserva {
  id: number;
  pista: Pista;
  fecha: string; // formato: "2025-05-22"
  hora: string;  // "18:00"
  estado: 'confirmada' | 'cancelada' | 'completada';
}