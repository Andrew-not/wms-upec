from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class OrdenRecepcion(models.Model):
    """
    Orden de recepción de mercadería de un proveedor.
    """
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PROCESO', 'En proceso'),
        ('RECIBIDA', 'Recibida'),
        ('CANCELADA', 'Cancelada'),
    ]

    numero = models.CharField(
        'Número de orden',
        max_length=20,
        unique=True,
        help_text='Ej: OC-2026-001'
    )
    proveedor = models.ForeignKey(
        'catalogo.Proveedor',
        on_delete=models.PROTECT,
        related_name='ordenes_recepcion',
        verbose_name='Proveedor'
    )
    fecha_emision = models.DateField('Fecha de emisión', auto_now_add=True)
    fecha_esperada = models.DateField('Fecha esperada de entrega')
    fecha_recepcion = models.DateField(
        'Fecha de recepción',
        null=True,
        blank=True
    )
    estado = models.CharField(
        'Estado',
        max_length=20,
        choices=ESTADOS,
        default='PENDIENTE'
    )
    documento_referencia = models.CharField(
        'Documento de referencia',
        max_length=100,
        blank=True,
        help_text='Factura, guía de remisión, etc.'
    )
    observaciones = models.TextField('Observaciones', blank=True)
    usuario_creacion = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='ordenes_creadas',
        verbose_name='Usuario creador'
    )
    usuario_recepcion = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='ordenes_recibidas',
        verbose_name='Usuario que recibió',
        null=True,
        blank=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Orden de recepción'
        verbose_name_plural = 'Órdenes de recepción'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.numero} - {self.proveedor.razon_social}'

    @property
    def total_lineas(self):
        return self.lineas.count()

    @property
    def total_unidades_esperadas(self):
        return sum(l.cantidad_esperada for l in self.lineas.all())

    @property
    def total_unidades_recibidas(self):
        return sum(l.cantidad_recibida for l in self.lineas.all())

    @property
    def porcentaje_recepcion(self):
        esperado = self.total_unidades_esperadas
        if esperado == 0:
            return 0
        return round((self.total_unidades_recibidas / esperado) * 100, 1)


class LineaRecepcion(models.Model):
    """
    Línea individual de una orden de recepción.
    """
    orden = models.ForeignKey(
        OrdenRecepcion,
        on_delete=models.CASCADE,
        related_name='lineas',
        verbose_name='Orden'
    )
    producto = models.ForeignKey(
        'catalogo.Producto',
        on_delete=models.PROTECT,
        related_name='lineas_recepcion',
        verbose_name='Producto'
    )
    cantidad_esperada = models.IntegerField(
        'Cantidad esperada',
        validators=[MinValueValidator(1)]
    )
    cantidad_recibida = models.IntegerField(
        'Cantidad recibida',
        default=0,
        validators=[MinValueValidator(0)]
    )
    ubicacion_destino = models.ForeignKey(
        'almacen.Ubicacion',
        on_delete=models.PROTECT,
        related_name='recepciones',
        verbose_name='Ubicación destino'
    )
    observacion = models.TextField('Observación', blank=True)
    fecha_recepcion = models.DateTimeField(
        'Fecha de recepción',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Línea de recepción'
        verbose_name_plural = 'Líneas de recepción'
        unique_together = [['orden', 'producto']]
        ordering = ['orden', 'producto']

    def __str__(self):
        return f'{self.producto.sku} x {self.cantidad_esperada}'

    @property
    def diferencia(self):
        return self.cantidad_recibida - self.cantidad_esperada

    @property
    def completa(self):
        return self.cantidad_recibida >= self.cantidad_esperada