from rest_framework import viewsets, permissions, generics
from .models import Usuario, Pista, Reserva, Membresia
from .permissions import AdminReadOnlyPermission, MembresiaPermission, ReservaPermission, PistaPermission
from .serializers import UsuarioSerializer, PistaSerializer, ReservaSerializer, MembresiaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from django.contrib.auth import login

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AdminReadOnlyPermission]  # Updated permission

class MembresiaViewSet(viewsets.ModelViewSet):
    queryset = Membresia.objects.all()
    serializer_class = MembresiaSerializer
    permission_classes = [MembresiaPermission]  # Updated permission

class PistaViewSet(viewsets.ModelViewSet):
    queryset = Pista.objects.all()
    serializer_class = PistaSerializer
    permission_classes = [PistaPermission]   # Basic authentication required

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [ReservaPermission]  # Updated permission

class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]  # Allow anyone to login

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({'message': 'Inicio de sesión exitoso'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)