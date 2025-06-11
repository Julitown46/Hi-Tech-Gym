from dateutil.relativedelta import relativedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from datetime import datetime, timedelta


class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Usuarios deben tener username')
        if not email:
            raise ValueError('Usuarios deben tener email')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('rol', 'superuser')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('rol') != 'superuser':
            raise ValueError('Superuser deben tener rol="superuser"')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deben tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deben tener is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    rol = models.CharField(
        max_length=20,
        choices=[
            ('superuser', 'Superuser'),
            ('admin', 'Admin'),
            ('usuario', 'Usuario')
        ],
        default='usuario'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UsuarioManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)

        if self.rol == 'superuser':
            self.is_superuser = True
            self.is_staff = True
        elif self.rol == 'admin':
            self.is_superuser = False
            self.is_staff = True
        else:
            self.is_superuser = False
            self.is_staff = False

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.reservas.filter(estado='confirmada').update(estado='cancelada')
        super().delete(*args, **kwargs)

    @property
    def membresia_activa(self):
        hoy = timezone.now().date()
        return self.membresias.filter(fecha_inicio__lte=hoy, fecha_fin__gte=hoy).exists()

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_admin(self):
        return self.is_staff

class Membresia(models.Model):
    usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        related_name='membresias'
    )
    fecha_inicio = models.DateField(editable=False)
    fecha_fin = models.DateField(editable=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.fecha_inicio = timezone.now().date()
            self.fecha_fin = self.fecha_inicio + relativedelta(months=1)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Membresía de {self.usuario} del {self.fecha_inicio} al {self.fecha_fin}"

class Pista(models.Model):
    nombre = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def delete(self, *args, **kwargs):
        self.activa = False
        self.save()

class Reserva(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    pista = models.ForeignKey(
        Pista,
        on_delete=models.PROTECT,
        limit_choices_to={'activa': True}
    )
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(
        max_length=20,
        choices=[
            ('confirmada', 'Confirmada'),
            ('cancelada', 'Cancelada'),
            ('completada', 'Completada')
        ],
        default='confirmada'
    )

    class Meta:
        unique_together = ['pista', 'fecha', 'hora']

    def clean(self):
        if self.fecha < timezone.now().date():
            raise ValidationError('No se pueden hacer reservas en fechas pasadas')

        if not self.usuario.membresia_activa and self.estado == 'confirmada':
            raise ValidationError('El usuario debe tener una membresía activa para reservar')

        if self.estado == 'confirmada':
            reservas_activas = Reserva.objects.filter(
                usuario=self.usuario,
                estado='confirmada'
            )
            if self.pk:
                reservas_activas = reservas_activas.exclude(pk=self.pk)

            if reservas_activas.count() >= 2:
                raise ValidationError('Ya tienes 2 reservas activas. Cancela alguna para hacer otra.')

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.estado == 'confirmada':
            now = timezone.now()
            reserva_datetime = timezone.make_aware(datetime.combine(self.fecha, self.hora))

            if now >= reserva_datetime + timedelta(minutes=20):
                self.estado = 'completada'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.usuario.username}"
