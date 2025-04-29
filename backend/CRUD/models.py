from django.db import models
from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    membresia_activa = models.BooleanField(default=False)
    rol = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('usuario', 'Usuario')], default='usuario')

    def __str__(self):
        return self.nombre

class Membresia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"Membresía de {self.usuario.nombre}"

class Pista(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    pista = models.ForeignKey(Pista, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(max_length=20, choices=[('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')])

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.usuario.nombre}"
