from datetime import date

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Usuario, Pista, Reserva, Membresia
from .permissions import AdminReadOnlyPermission, ReservaPermission, PistaPermission, MembresiaPermission
from .serializers import UsuarioSerializer, PistaSerializer, ReservaSerializer, MembresiaSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from django.contrib.auth import login, logout


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [AdminReadOnlyPermission()]

class MembresiaViewSet(viewsets.ModelViewSet):
    queryset = Membresia.objects.all()
    serializer_class = MembresiaSerializer
    permission_classes = [MembresiaPermission]

    @action(detail=False, methods=['delete'], url_path='cancelar', permission_classes=[IsAuthenticated])
    def cancelar_membresia(self, request):
        usuario = request.user
        hoy = date.today()

        membresias = Membresia.objects.filter(
            usuario=usuario,
            fecha_inicio__lte=hoy,
            fecha_fin__gte=hoy
        )

        if not membresias.exists():
            return Response({"detail": "No tienes membresía activa."}, status=status.HTTP_400_BAD_REQUEST)

        membresias.delete()

        Reserva.objects.filter(usuario=usuario, estado='confirmada').update(estado='cancelada')

        return Response({"detail": "Membresía y reservas canceladas correctamente."}, status=status.HTTP_204_NO_CONTENT)

class PistaViewSet(viewsets.ModelViewSet):
    queryset = Pista.objects.all()
    serializer_class = PistaSerializer
    permission_classes = [PistaPermission]

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)

            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'membresia_activa': user.membresia_activa,
                'rol': user.rol,
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout completado"}, status=status.HTTP_200_OK)

@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({'csrfToken': request.META.get('CSRF_COOKIE')})


class MisReservasView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reservas = Reserva.objects.filter(usuario=request.user).order_by('-fecha', '-hora')
        serializer = ReservaSerializer(reservas, many=True)
        return Response(serializer.data)