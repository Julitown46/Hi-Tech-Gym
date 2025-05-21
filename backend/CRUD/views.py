from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets, permissions, generics
from .models import Usuario, Pista, Reserva, Membresia
from .permissions import AdminReadOnlyPermission, MembresiaPermission, ReservaPermission, PistaPermission
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

class PistaViewSet(viewsets.ModelViewSet):
    queryset = Pista.objects.all()
    serializer_class = PistaSerializer
    permission_classes = [PistaPermission]

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [ReservaPermission]

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