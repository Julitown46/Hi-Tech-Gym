import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-contacto',
  imports: [CommonModule],
  templateUrl: './contacto.component.html',
  styleUrl: './contacto.component.css'
})
export class ContactoComponent {

  reviews = [
  { text: 'Las pistas son de primera calidad y el sistema de reservas es muy fácil de usar.', author: 'Carlos G.' },
  { text: 'Me encanta entrenar aquí, todo es muy cómodo y moderno.', author: 'Laura P.' },
  { text: 'El mejor gimnasio de la ciudad, sin duda.', author: 'Mario R.' },
  { text: 'Las clases dirigidas son espectaculares, los monitores son muy profesionales.', author: 'Ana L.' },
  { text: 'El ambiente es increíble, te sientes motivado desde que entras.', author: 'Javier M.' }
];
}
