from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Membresia, Pista, Reserva

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'membresia_activa', 'is_active', 'is_staff')
    list_filter = ('rol', 'membresia_activa', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Información personal', {'fields': ('rol', 'membresia_activa')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'rol', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Membresia)
admin.site.register(Pista)
admin.site.register(Reserva)