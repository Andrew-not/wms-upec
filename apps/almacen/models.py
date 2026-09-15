from django.db import models
from django.conf import settings
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
    Área dentro de la bodega.
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
    Posición exacta dentro de una zona.
    """
    TIPOS_UBICACION = (
        ('ESTANTE', 'Estante'),
        ('PISO', 'Piso'),
        ('REFRIGERADO', 'Refrigerado'),
        ('CUARENTENA', 'Cuarentena'),
    )

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
    tipo_ubicacion = models.CharField(
        'Tipo de ubicación',
        max_length=20,
        choices=TIPOS_UBICACION,
        default='ESTANTE'
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
    peso_maximo_kg = models.DecimalField(
        'Peso máximo (kg)',
        max_digits=8,
        decimal_places=2,
        default=100,
        validators=[MinValueValidator(0)]
    )
    volumen_m3 = models.DecimalField(
        'Volumen (m³)',
        max_digits=8,
        decimal_places=3,
        default=1,
        validators=[MinValueValidator(0)]
    )
    coordenada_x = models.IntegerField('Coordenada X', default=0)
    coordenada_y = models.IntegerField('Coordenada Y', default=0)
    activo = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'
        ordering = ['codigo']
        indexes = [
            models.Index(fields=['codigo']),
            models.Index(fields=['zona', 'activo']),
        ]

    def __str__(self):
        return self.codigo

    @property
    def ocupacion_actual(self):
        from django.db.models import Sum
        total = self.existencias.aggregate(total=Sum('cantidad'))['total']
        return total or 0

    @property
    def porcentaje_ocupacion(self):
        if self.capacidad_maxima == 0:
            return 0
        return round((self.ocupacion_actual / self.capacidad_maxima) * 100, 1)

    @property
    def disponible(self):
        return self.ocupacion_actual < self.capacidad_maxima


class MovimientoUbicacion(models.Model):
    """
    Historial de movimientos dentro de una ubicación.
    """
    TIPOS = (
        ('INGRESO', 'Ingreso'),
        ('RETIRO', 'Retiro'),
        ('TRASLADO', 'Traslado'),
    )

    ubicacion = models.ForeignKey(
        Ubicacion,
        on_delete=models.PROTECT,
        related_name='movimientos_ubicacion',
        verbose_name='Ubicación'
    )
    producto = models.ForeignKey(
        'catalogo.Producto',
        on_delete=models.PROTECT,
        related_name='movimientos_ubicacion',
        verbose_name='Producto'
    )
    cantidad = models.IntegerField(
        'Cantidad',
        validators=[MinValueValidator(1)]
    )
    tipo = models.CharField('Tipo', max_length=20, choices=TIPOS)
    fecha = models.DateTimeField('Fecha', auto_now_add=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='movimientos_ubicacion',
        verbose_name='Usuario'
    )
    observacion = models.TextField('Observación', blank=True)

    class Meta:
        verbose_name = 'Movimiento de ubicación'
        verbose_name_plural = 'Movimientos de ubicación'
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.producto.sku} @ {self.ubicacion.codigo}'