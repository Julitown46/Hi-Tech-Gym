# reservas/signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from datetime import date
from .models import Membresia, Usuario

@receiver(post_delete, sender=Membresia)
def actualizar_membresia_tras_eliminar(sender, instance, **kwargs):
    usuario = instance.usuario
    hoy = date.today()

    tiene_membresia_activa = Membresia.objects.filter(
        usuario=usuario,
        fecha_inicio__lte=hoy,
        fecha_fin__gte=hoy
    ).exists()

    usuario.membresia_activa = tiene_membresia_activa
    usuario.save()
