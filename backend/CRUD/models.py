from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework.exceptions import ValidationError


class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    membresia_activa = models.BooleanField(default=False)
    rol = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('usuario', 'Usuario')], default='usuario')
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
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.reservas.filter(estado='confirmada').update(estado='cancelada')
        super().delete(*args, **kwargs)

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
        Usuario,
        on_delete=models.CASCADE,
        related_name='membresias'
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def clean(self):
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio > self.fecha_fin:
                raise ValidationError('La fecha de inicio debe ser anterior a la fecha fin')
            if self.fecha_inicio < timezone.now().date():
                raise ValidationError('La fecha de inicio no puede ser en el pasado')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Pista(models.Model):
    nombre = models.CharField(max_length=100)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

    def delete(self, *args, **kwargs):
        # Soft delete - en lugar de borrar, desactivamos
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
        on_delete=models.PROTECT,  # Evita borrado de pistas con reservas
        limit_choices_to={'activa': True}
    )
    fecha = models.DateField()
    hora = models.TimeField()
    estado = models.CharField(
        max_length=20,
        choices=[('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')],
        default='confirmada'
    )

    class Meta:
        unique_together = ['pista', 'fecha', 'hora']

    def clean(self):
        if self.fecha < timezone.now().date():
            raise ValidationError('No se pueden hacer reservas en fechas pasadas')
        if not self.usuario.membresia_activa and self.estado == 'confirmada':
            raise ValidationError('El usuario debe tener una membresía activa para reservar')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.fecha} {self.hora} - {self.usuario.username}"
