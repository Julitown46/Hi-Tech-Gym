from rest_framework import permissions


class AdminReadOnlyPermission(permissions.BasePermission):
    """
    Permite:
    - Crear usuarios a cualquiera
    - Admin puede ver la lista de usuarios
    - Usuarios pueden gestionar su propio perfil
    """

    def has_permission(self, request, view):
        if request.method == 'POST':  # Crear usuario
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        if request.method == 'GET' and 'pk' not in view.kwargs:
            # Lista de usuarios - solo admin
            return request.user.rol == 'admin'

        return True

    def has_object_permission(self, request, view, obj):
        # Usuario puede gestionar su propio perfil o admin puede gestionar cualquiera
        return obj.id == request.user.id or request.user.rol == 'admin'

class MembresiaPermission(permissions.BasePermission):
    """
    Los usuarios pueden crear su propia membresía. Solo los admin pueden ver/modificar otras.
    """

    def has_permission(self, request, view):
        # Permitir que cualquier usuario autenticado cree su propia membresía (POST)
        if request.method == 'POST':
            return request.user and request.user.is_authenticated

        # Para otros métodos, solo admin
        return request.user and request.user.is_authenticated and request.user.rol == 'admin'

    def has_object_permission(self, request, view, obj):
        # Solo el admin puede modificar/eliminar cualquier objeto
        return request.user.rol == 'admin'

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
    Todos pueden ver pistas (GET).
    """

    def has_permission(self, request, view):
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_authenticated and request.user.rol == 'admin'
        return True  # Permitir GET sin autenticación
