from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import serializers, permissions, generics
from .models import Usuario, Membresia, Pista, Reserva
from datetime import date, timedelta


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
        read_only_fields = ['usuario', 'fecha_inicio', 'fecha_fin']

    def create(self, validated_data):
        usuario = self.context['request'].user
        hoy = date.today()
        fin = hoy + timedelta(days=30)

        return Membresia.objects.create(
            usuario=usuario,
            fecha_inicio=hoy,
            fecha_fin=fin
        )

class PistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pista
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    pista = serializers.PrimaryKeyRelatedField(queryset=Pista.objects.filter(activa=True))

    class Meta:
        model = Reserva
        fields = '__all__'
        read_only_fields = ['usuario']

    def validate(self, data):
        request = self.context.get('request')
        if not request or not hasattr(request, 'user'):
            raise serializers.ValidationError("No se ha proporcionado un usuario autenticado.")

        usuario = request.user
        fecha = data.get('fecha')
        hora = data.get('hora')
        pista = data.get('pista')

        if not pista or not fecha or not hora:
            raise serializers.ValidationError("Faltan campos obligatorios (pista, fecha u hora)")

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

        reservas_activas = Reserva.objects.filter(
            usuario=usuario,
            estado='confirmada'
        ).count()

        if reservas_activas >= 2:
            raise serializers.ValidationError("Ya tienes 2 reservas activas. Cancela alguna para poder hacer otra.")

        if Reserva.objects.filter(
                pista=pista,
                fecha=fecha,
                hora=hora
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