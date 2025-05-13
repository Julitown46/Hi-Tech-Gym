from django.test import TestCase
from datetime import date, timedelta
from CRUD.models import Usuario, Membresia, Pista, Reserva
from CRUD.serializers import ReservaSerializer
from django.core.exceptions import ValidationError


class ReservaTests(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(username="Juan", email="juan@mail.com")
        self.pista = Pista.objects.create(nombre="Pista 1")
        hoy = date.today()
        self.membresia = Membresia.objects.create(
            usuario=self.usuario,
            fecha_inicio=hoy,
            fecha_fin=hoy + timedelta(days=30)
        )

    def test_crear_reserva_valida(self):
        reserva = Reserva.objects.create(
            usuario=self.usuario,
            pista=self.pista,
            fecha=date.today(),
            hora='10:00',
            estado='confirmada'
        )
        self.assertEqual(reserva.usuario, self.usuario)
        self.assertEqual(reserva.estado, 'confirmada')

    def test_no_permite_reservas_duplicadas(self):
        Reserva.objects.create(
            usuario=self.usuario,
            pista=self.pista,
            fecha=date.today(),
            hora='11:00',
            estado='confirmada'
        )
        with self.assertRaises(ValidationError):
            Reserva.objects.create(
                usuario=self.usuario,
                pista=self.pista,
                fecha=date.today(),
                hora='11:00',
                estado='confirmada'
            )

    def test_cancelar_reserva(self):
        reserva = Reserva.objects.create(
            usuario=self.usuario,
            pista=self.pista,
            fecha=date.today(),
            hora='12:00',
            estado='confirmada'
        )
        reserva.estado = 'cancelada'
        reserva.save()
        self.assertEqual(reserva.estado, 'cancelada')

    def test_no_permite_reserva_fecha_pasada(self):
        fecha_pasada = date.today() - timedelta(days=1)
        reserva_data = {
            'usuario': self.usuario.id,
            'pista': self.pista.id,
            'fecha': fecha_pasada,
            'hora': '15:00',
            'estado': 'confirmada'
        }
        serializer = ReservaSerializer(data=reserva_data)
        self.assertFalse(serializer.is_valid())

    def test_limite_reservas_por_dia(self):
        hoy = date.today()
        # Create first two reservations
        Reserva.objects.create(
            usuario=self.usuario,
            pista=self.pista,
            fecha=hoy,
            hora='16:00',
            estado='confirmada'
        )
        Reserva.objects.create(
            usuario=self.usuario,
            pista=self.pista,
            fecha=hoy,
            hora='17:00',
            estado='confirmada'
        )

        # Try to create a third reservation - should fail
        with self.assertRaises(Exception):
            Reserva.objects.create(
                usuario=self.usuario,
                pista=self.pista,
                fecha=hoy,
                hora='18:00',
                estado='confirmada'
            )

    def test_no_permite_reserva_fecha_pasada(self):
        fecha_pasada = date.today() - timedelta(days=1)
        with self.assertRaises(Exception):  # Using model validation
            Reserva.objects.create(
                usuario=self.usuario,
                pista=self.pista,
                fecha=fecha_pasada,
                hora='15:00',
                estado='confirmada'
            )