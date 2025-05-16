import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-inicio',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './inicio.component.html',
  styleUrl: './inicio.component.css'
})
export class InicioComponent {
  cards = [
    { img: 'clases.webp', text: 'Ofrecemos una amplia variedad de clases como Yoga, Zumba, Spinning, Crossfit y Pilates. Nuestros instructores certificados adaptan cada clase a todos los niveles, desde principiantes hasta expertos. Mejora tu salud física y mental en un ambiente dinámico y motivador.' },
    { img: 'entrenamiento.jpg', text: 'Disfruta de acceso completo a nuestra sala de entrenamiento equipada con máquinas de última generación, pesas libres y zonas de cardio. Nuestros técnicos están disponibles para asesorarte y ayudarte a lograr tus objetivos de fuerza, resistencia y bienestar.' },
    { img: 'padel.webp', text: 'Reserva rápida y sencilla desde nuestra web para disfrutar de nuestras pistas de pádel profesionales. Disponemos de iluminación nocturna y alquiler de material. Participa en nuestras ligas y torneos mensuales y mejora tu nivel en un ambiente deportivo y social.' }
  ];
}
