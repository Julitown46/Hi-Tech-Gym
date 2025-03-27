export interface Pago {
    id_pago: number;
    id_reserva: number;
    id_membresia: number;
    importe: number;
    fecha: string;
    estado: string;
}