from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Membresia, Pista, Reserva

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'rol', 'is_active', 'is_staff')
    list_filter = ('rol', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Información personal', {'fields': ('rol',)}),
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

class MembresiaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_inicio', 'fecha_fin')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('fecha_inicio', 'fecha_fin', 'usuario')
        return ()


admin.site.register(Usuario, CustomUserAdmin)
admin.site.register(Membresia, MembresiaAdmin)
admin.site.register(Pista)
admin.site.register(Reserva)