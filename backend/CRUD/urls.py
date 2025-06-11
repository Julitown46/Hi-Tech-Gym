from django.urls import path
from rest_framework.routers import DefaultRouter
from CRUD.views import UsuarioViewSet, PistaViewSet, ReservaViewSet, MembresiaViewSet, LoginView, LogoutView, \
    get_csrf, MisReservasView, ReservasConfirmadasView

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'pistas', PistaViewSet)
router.register(r'membresias', MembresiaViewSet)
router.register(r'reservas', ReservaViewSet)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('csrf/', get_csrf, name='csrf'),
    path('reservas/mis-reservas/', MisReservasView.as_view(), name='mis-reservas'),
    path('reservas/confirmadas/', ReservasConfirmadasView.as_view()),
] + router.urls