from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado para C.TECH.
    """
    
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('JEFE', 'Jefe'),
        ('OPERARIO', 'Operario'),
        ('CONSULTA', 'Consulta'),
    )
    
    cedula = models.CharField(
        'Cédula',
        max_length=10,
        unique=True,
        blank=True,
        null=True
    )
    telefono = models.CharField(
        'Teléfono',
        max_length=15,
        blank=True,
        null=True
    )
    rol = models.CharField(
        'Rol en el sistema',
        max_length=20,
        choices=ROLES,
        default='CONSULTA'
    )
    cargo = models.CharField(
        'Cargo',
        max_length=100,
        blank=True,
        help_text='Ej: Jefe de Bodega, Técnico, Vendedor'
    )
    fecha_registro = models.DateTimeField(
        'Fecha de registro',
        auto_now_add=True
    )
    activo = models.BooleanField(
        'Activo',
        default=True
    )
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-date_joined']
    
    def __str__(self):
        nombre = self.get_full_name().strip()
        if nombre:
            return f"{nombre} - {self.get_rol_display()}"
        return f"{self.username} - {self.get_rol_display()}"