from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.rol == 'admin'

class CanCreateAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' and request.data.get('rol') == 'admin':
            return request.user and request.user.is_authenticated and request.user.rol == 'admin'
        return True

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permite al propietario de un objeto editarlo.
    Permite a los administradores editar cualquier objeto.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.rol == 'admin':
            return True
        return obj.usuario == request.user