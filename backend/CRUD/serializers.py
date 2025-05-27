from django.contrib.auth import authenticate
from rest_framework import serializers, permissions, generics
from .models import Usuario, Membresia, Pista, Reserva
from datetime import date

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        read_only_fields = ('id',)

    def validate(self, data):
        if data.get('rol') == 'admin':
            request = self.context.get('request')
            if not request or not request.user.is_authenticated or request.user.rol != 'admin':
                raise serializers.ValidationError("Solo los administradores pueden crear otros administradores")

        if data.get('is_superuser'):
            request = self.context.get('request')
            if not request or not request.user.is_authenticated or not request.user.is_superuser:
                raise serializers.ValidationError("Solo los superusuarios pueden crear otros superusuarios")

        return data

class MembresiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membresia
        fields = ['id', 'usuario', 'fecha_inicio', 'fecha_fin']
        read_only_fields = ['fecha_inicio', 'fecha_fin', 'usuario']

    def create(self, validated_data):
        membresia = super().create(validated_data)
        self.actualizar_estado_usuario(membresia.usuario)
        return membresia

    def update(self, instance, validated_data):
        membresia = super().update(instance, validated_data)
        self.actualizar_estado_usuario(membresia.usuario)
        return membresia

    def actualizar_estado_usuario(self, usuario):
        hoy = date.today()
        tiene_membresia_activa = Membresia.objects.filter(
            usuario=usuario,
            fecha_inicio__lte=hoy,
            fecha_fin__gte=hoy
        ).exists()

        usuario.membresia_activa = tiene_membresia_activa
        usuario.save()

class PistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pista
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'

    def validate(self, data):
        usuario = data.get('usuario')
        fecha = data.get('fecha')

        # Check membership
        hoy = date.today()
        membresia_valida = Membresia.objects.filter(
            usuario=usuario,
            fecha_inicio__lte=hoy,
            fecha_fin__gte=hoy
        ).exists()

        if not membresia_valida:
            raise serializers.ValidationError("El usuario no tiene una membresía activa y vigente.")

        if fecha < hoy:
            raise serializers.ValidationError("No se pueden hacer reservas para fechas pasadas")

        reservas_dia = Reserva.objects.filter(
            usuario=usuario,
            fecha=fecha,
            estado='confirmada'
        ).count()

        if reservas_dia >= 2:
            raise serializers.ValidationError("Has alcanzado el límite de reservas para este día")

        if Reserva.objects.filter(
                pista=data['pista'],
                fecha=fecha,
                hora=data['hora']
        ).exists():
            raise serializers.ValidationError("Ya existe una reserva para esta pista en esta fecha y hora")

        return data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError('La cuenta del usuario está desactivada.')
                data['user'] = user
            else:
                raise serializers.ValidationError('Credenciales inválidas.')
        else:
            raise serializers.ValidationError('Debes incluir tanto el nombre de usuario como la contraseña.')

        return data