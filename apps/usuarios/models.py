from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado para el WMS
    """
    
    # Roles posibles en el sistema
    ROLES = (
        ('ADMIN', 'Administrador'),
        ('JEFE_BODEGA', 'Jefe de Bodega'),
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
            return f"{nombre} ({self.username}) - {self.get_rol_display()}"
        return f"{self.username} - {self.get_rol_display()}"