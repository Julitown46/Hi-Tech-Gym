from django.test import TestCase
from datetime import date, timedelta, time
from types import SimpleNamespace

from django.contrib.auth import get_user_model
from CRUD.models import Pista, Membresia, Reserva
from CRUD.serializers import ReservaSerializer
from rest_framework.exceptions import ValidationError

User = get_user_model()

class MembresiaTests(TestCase):

    def setUp(self):
        self.hoy = date.today()
        self.pista = Pista.objects.create(nombre='Pista Test')

    def test_no_se_puede_reservar_sin_membresia_activa(self):
        usuario = User.objects.create_user(
            username='nomembresia',
            email='no@correo.com',
            password='pass'
        )

        data = {
            'pista': self.pista.id,
            'fecha': self.hoy + timedelta(days=1),
            'hora': time(10, 0)
        }

        context = {'request': SimpleNamespace(user=usuario)}
        serializer = ReservaSerializer(data=data, context=context)
        self.assertFalse(serializer.is_valid())
        self.assertIn("membresía activa", str(serializer.errors).lower())

    def test_se_puede_reservar_con_membresia_activa(self):
        usuario = User.objects.create_user(
            username='conmembresia',
            email='con@correo.com',
            password='pass'
        )

        Membresia.objects.create(
            usuario=usuario,
            fecha_inicio=self.hoy - timedelta(days=5),
            fecha_fin=self.hoy + timedelta(days=5)
        )

        data = {
            'pista': self.pista.id,
            'fecha': self.hoy + timedelta(days=1),
            'hora': time(11, 0)
        }

        context = {'request': SimpleNamespace(user=usuario)}
        serializer = ReservaSerializer(data=data, context=context)

        is_valid = serializer.is_valid()
        print("Errores del serializer:", serializer.errors)

        self.assertTrue(is_valid, serializer.errors)

