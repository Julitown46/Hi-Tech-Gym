from rest_framework import permissions

class AdminReadOnlyPermission(permissions.BasePermission):
    """
    Permite crear usuarios y hacer login a cualquiera,
    pero solo los admin pueden ver la lista de usuarios.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':  # Crear usuario o login
            return True
        return request.user and request.user.is_authenticated and request.user.rol == 'admin'

class MembresiaPermission(permissions.BasePermission):
    """
    Solo los administradores pueden gestionar las membresías.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol == 'admin'

class ReservaPermission(permissions.BasePermission):
    """
    Solo usuarios con membresía activa pueden hacer reservas.
    """
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            (request.user.membresia_activa or request.user.rol == 'admin')
        )

    def has_object_permission(self, request, view, obj):
        if request.user.rol == 'admin':
            return True
        return obj.usuario == request.user and request.user.membresia_activa


class PistaPermission(permissions.BasePermission):
    """
    Solo los admin pueden crear/modificar pistas.
    Solo usuarios autenticados pueden verlas.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.rol == 'admin'

        return True