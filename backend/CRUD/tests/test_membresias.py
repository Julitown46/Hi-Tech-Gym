from django.test import TestCase
from datetime import date, timedelta
from CRUD.models import Usuario, Membresia, Pista, Reserva
from CRUD.serializers import ReservaSerializer

class MembresiaTests(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create(username="Juan", email="juan@mail.com")
        self.pista = Pista.objects.create(nombre="Pista 1")

    def test_usuario_no_tiene_membresia_activa(self):
        self.assertFalse(self.usuario.membresia_activa)

    def test_membresia_activa_se_actualiza_al_crear(self):
        hoy = date.today()
        Membresia.objects.create(usuario=self.usuario, fecha_inicio=hoy, fecha_fin=hoy + timedelta(days=10))
        self.usuario.refresh_from_db()
        self.assertTrue(self.usuario.membresia_activa)

    def test_membresia_activa_se_actualiza_al_eliminar(self):
        hoy = date.today()
        membresia = Membresia.objects.create(usuario=self.usuario, fecha_inicio=hoy, fecha_fin=hoy + timedelta(days=10))
        membresia.delete()
        self.usuario.refresh_from_db()
        self.assertFalse(self.usuario.membresia_activa)

    def test_no_se_puede_reservar_sin_membresia_activa(self):
        reserva_data = {
            'usuario': self.usuario.id,
            'pista': self.pista.id,
            'fecha': date.today(),
            'hora': '18:00',
            'estado': 'confirmada'
        }
        serializer = ReservaSerializer(data=reserva_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_se_puede_reservar_con_membresia_activa(self):
        hoy = date.today()
        Membresia.objects.create(usuario=self.usuario, fecha_inicio=hoy, fecha_fin=hoy + timedelta(days=5))
        reserva_data = {
            'usuario': self.usuario.id,
            'pista': self.pista.id,
            'fecha': hoy,
            'hora': '19:00',
            'estado': 'confirmada'
        }
        serializer = ReservaSerializer(data=reserva_data)
        self.assertTrue(serializer.is_valid())
