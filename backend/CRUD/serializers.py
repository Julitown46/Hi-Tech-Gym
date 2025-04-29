from rest_framework import serializers
from .models import Usuario, Membresia, Pista, Reserva
from datetime import date

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'
        read_only_fields = ('email',)

class MembresiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membresia
        fields = '__all__'
        read_only_fields = ('usuario',)

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

            hoy = date.today()
            membresia_valida = Membresia.objects.filter(
                usuario=usuario,
                fecha_inicio__lte=hoy,
                fecha_fin__gte=hoy
            ).exists()

            if not membresia_valida:
                raise serializers.ValidationError("El usuario no tiene una membresía activa y vigente.")

            return data