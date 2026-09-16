from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Admin personalizado para el modelo Usuario.
    """
    
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'cedula', 'rol', 'cargo', 'is_active', 'is_staff'
    )
    list_filter = ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'cedula')
    ordering = ('username',)
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        (_('Información personal'), {
            'fields': ('first_name', 'last_name', 'email', 'cedula', 'telefono')
        }),
        (_('Rol y cargo'), {
            'fields': ('rol', 'cargo')
        }),
        (_('Permisos'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        (_('Fechas importantes'), {
            'fields': ('last_login', 'date_joined', 'fecha_registro')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        (_('Información personal'), {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'cedula', 'telefono'),
        }),
        (_('Rol y cargo'), {
            'classes': ('wide',),
            'fields': ('rol', 'cargo'),
        }),
        (_('Permisos'), {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
    )
    
    readonly_fields = ('fecha_registro', 'last_login', 'date_joined')