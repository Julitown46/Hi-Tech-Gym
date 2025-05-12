from django.urls import path
from rest_framework.routers import DefaultRouter
from CRUD.views import UsuarioViewSet, PistaViewSet, ReservaViewSet, MembresiaViewSet, LoginView, LogoutView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'pistas', PistaViewSet)
router.register(r'membresias', MembresiaViewSet)
router.register(r'reservas', ReservaViewSet)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
] + router.urls