from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'email', 'cedula', 'rol', 'is_active')
    list_filter = ('rol', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'cedula')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email', 'cedula', 'telefono')}),
        ('Permisos', {'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'cedula', 'rol', 'password1', 'password2'),
        }),
    )