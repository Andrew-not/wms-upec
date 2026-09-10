from django.db import models
from django.core.validators import MinValueValidator


class Bodega(models.Model):
    """
    Instalación física donde se almacenan los dispositivos.
    """
    codigo = models.CharField('Código', max_length=20, unique=True)
    nombre = models.CharField('Nombre', max_length=200)
    direccion = models.CharField('Dirección', max_length=300, blank=True)
    ciudad = models.CharField('Ciudad', max_length=100, blank=True)
    activo = models.BooleanField('Activo', default=True)
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)

    class Meta:
        verbose_name = 'Bodega'
        verbose_name_plural = 'Bodegas'
        ordering = ['codigo']

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'


class Zona(models.Model):
    """
    Área dentro de la bodega. Ej: Recepción, Almacenaje, Reparación.
    """
    TIPOS = (
        ('RECEPCION', 'Recepción'),
        ('ALMACENAJE', 'Almacenaje'),
        ('PICKING', 'Picking'),
        ('DESPACHO', 'Despacho'),
        ('CUARENTENA', 'Cuarentena'),
        ('SERVICIO', 'Servicio Técnico'),
        ('PERSONALIZACION', 'Personalización'),
    )

    bodega = models.ForeignKey(
        Bodega,
        on_delete=models.PROTECT,
        related_name='zonas',
        verbose_name='Bodega'
    )
    codigo = models.CharField('Código', max_length=20)
    nombre = models.CharField('Nombre', max_length=200)
    tipo = models.CharField('Tipo de zona', max_length=20, choices=TIPOS)
    activo = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = 'Zona'
        verbose_name_plural = 'Zonas'
        unique_together = [['bodega', 'codigo']]
        ordering = ['bodega', 'codigo']

    def __str__(self):
        return f'{self.bodega.codigo}-{self.codigo} - {self.nombre}'


class Ubicacion(models.Model):
    """
    Posición exacta dentro de una zona. Formato: pasillo-rack-nivel.
    Ej: B1-Z1-E1 (Bodega 1, Zona 1, Estante 1)
    """
    codigo = models.CharField(
        'Código',
        max_length=50,
        unique=True,
        help_text='Formato: B{num}-Z{num}-E{num}. Ej: B1-Z1-E1'
    )
    zona = models.ForeignKey(
        Zona,
        on_delete=models.PROTECT,
        related_name='ubicaciones',
        verbose_name='Zona'
    )
    pasillo = models.CharField('Pasillo', max_length=20, blank=True)
    rack = models.CharField('Rack', max_length=20, blank=True)
    nivel = models.CharField('Nivel', max_length=20, blank=True)
    posicion = models.CharField('Posición', max_length=20, blank=True)
    capacidad_maxima = models.PositiveIntegerField(
        'Capacidad máxima (unidades)',
        default=100,
        validators=[MinValueValidator(1)]
    )
    activo = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'
        ordering = ['codigo']
        indexes = [models.Index(fields=['codigo'])]

    def __str__(self):
        return self.codigo

    @property
    def ocupacion_actual(self):
        """Suma de unidades almacenadas en esta ubicación."""
        from django.db.models import Sum
        total = self.existencias.aggregate(total=Sum('cantidad'))['total']
        return total or 0

    @property
    def porcentaje_ocupacion(self):
        """Porcentaje de ocupación respecto a la capacidad máxima."""
        if self.capacidad_maxima == 0:
            return 0
        return round((self.ocupacion_actual / self.capacidad_maxima) * 100, 1)

    @property
    def disponible(self):
        """True si hay espacio disponible en la ubicación."""
        return self.ocupacion_actual < self.capacidad_maxima