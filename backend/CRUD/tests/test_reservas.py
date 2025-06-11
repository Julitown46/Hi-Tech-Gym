from datetime import date, time, timedelta
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from CRUD.models import Usuario, Pista, Membresia, Reserva


class ReservaModelTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username='julian',
            email='julian@example.com',
            password='testpass'
        )
        self.pista = Pista.objects.create(nombre='Pista 1', activa=True)

    def test_reserva_valida(self):
        Membresia.objects.create(
            usuario=self.usuario,
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=30)
        )
        reserva = Reserva(
            usuario=self.usuario,
            pista=self.pista,
            fecha=date.today() + timedelta(days=1),
            hora=time(10, 0)
        )
        try:
            reserva.full_clean()
            reserva.save()
        except ValidationError:
            self.fail("La reserva válida no debería lanzar excepción")

    def test_reserva_en_fecha_pasada(self):
        reserva = Reserva(
            usuario=self.usuario,
            pista=self.pista,
            fecha=date.today() - timedelta(days=1),
            hora=time(10, 0)
        )
        with self.assertRaises(ValidationError) as context:
            reserva.full_clean()
        self.assertIn('No se pueden hacer reservas en fechas pasadas', str(context.exception))

    def test_reserva_sin_membresia_activa(self):
        reserva = Reserva(
            usuario=self.usuario,
            pista=self.pista,
            fecha=date.today() + timedelta(days=1),
            hora=time(10, 0)
        )
        with self.assertRaises(ValidationError) as context:
            reserva.full_clean()
        self.assertIn('El usuario debe tener una membresía activa para reservar', str(context.exception))

    def test_reserva_tercera_confirmada(self):
        Membresia.objects.create(
            usuario=self.usuario,
            fecha_inicio=date.today(),
            fecha_fin=date.today() + timedelta(days=30)
        )
        for i in range(2):
            Reserva.objects.create(
                usuario=self.usuario,
                pista=self.pista,
                fecha=date.today() + timedelta(days=1+i),
                hora=time(10, 0),
                estado='confirmada'
            )
        reserva = Reserva(
            usuario=self.usuario,
            pista=self.pista,
            fecha=date.today() + timedelta(days=3),
            hora=time(10, 0),
            estado='confirmada'
        )
        with self.assertRaises(ValidationError) as context:
            reserva.full_clean()
        self.assertIn('Ya tienes 2 reservas activas', str(context.exception))
