from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Existencia(models.Model):
    """
    Saldo actual de un producto en una ubicación específica.
    La combinación producto + ubicación es ÚNICA.
    """
    producto = models.ForeignKey(
        'catalogo.Producto',
        on_delete=models.PROTECT,
        related_name='existencias',
        verbose_name='Producto'
    )
    ubicacion = models.ForeignKey(
        'almacen.Ubicacion',
        on_delete=models.PROTECT,
        related_name='existencias',
        verbose_name='Ubicación'
    )
    cantidad = models.IntegerField(
        'Cantidad',
        default=0,
        validators=[MinValueValidator(0)]
    )
    cantidad_reservada = models.IntegerField(
        'Cantidad reservada',
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Unidades comprometidas en pedidos pendientes'
    )
    fecha_actualizacion = models.DateTimeField(
        'Última actualización',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Existencia'
        verbose_name_plural = 'Existencias'
        unique_together = [['producto', 'ubicacion']]
        ordering = ['producto', 'ubicacion']
        indexes = [
            models.Index(fields=['producto', 'ubicacion']),
        ]

    def __str__(self):
        return f'{self.producto.sku} @ {self.ubicacion.codigo}: {self.cantidad}'

    @property
    def cantidad_disponible(self):
        """Cantidad libre (no reservada)."""
        return self.cantidad - self.cantidad_reservada


class Movimiento(models.Model):
    """
    Kardex: registro histórico de TODOS los movimientos del almacén.
    Es de SOLO LECTURA: no se edita ni se borra nunca.
    """
    TIPOS = (
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('TRASLADO', 'Traslado'),
        ('AJUSTE_POS', 'Ajuste positivo'),
        ('AJUSTE_NEG', 'Ajuste negativo'),
        ('DEVOLUCION', 'Devolución'),
        ('SERVICIO', 'Envío a servicio técnico'),
        ('PERSONALIZACION', 'Envío a personalización'),
    )

    tipo = models.CharField('Tipo de movimiento', max_length=20, choices=TIPOS)
    producto = models.ForeignKey(
        'catalogo.Producto',
        on_delete=models.PROTECT,
        related_name='movimientos',
        verbose_name='Producto'
    )
    cantidad = models.IntegerField(
        'Cantidad',
        validators=[MinValueValidator(1)]
    )
    ubicacion_origen = models.ForeignKey(
        'almacen.Ubicacion',
        on_delete=models.PROTECT,
        related_name='movimientos_salida',
        verbose_name='Ubicación origen',
        null=True,
        blank=True
    )
    ubicacion_destino = models.ForeignKey(
        'almacen.Ubicacion',
        on_delete=models.PROTECT,
        related_name='movimientos_entrada',
        verbose_name='Ubicación destino',
        null=True,
        blank=True
    )
    documento = models.CharField(
        'Documento de referencia',
        max_length=100,
        blank=True,
        help_text='N° de orden, factura, guía, etc.'
    )
    observacion = models.TextField('Observación', blank=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='movimientos',
        verbose_name='Usuario responsable'
    )
    fecha = models.DateTimeField('Fecha y hora', auto_now_add=True)
    fecha_movimiento = models.DateField(
        'Fecha del movimiento',
        null=True,
        blank=True,
        help_text='Fecha real del movimiento (puede diferir de la fecha de registro)'
    )

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos (Kardex)'
        ordering = ['-fecha']
        indexes = [
            models.Index(fields=['-fecha']),
            models.Index(fields=['producto', '-fecha']),
            models.Index(fields=['tipo']),
        ]

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.producto.sku} x{self.cantidad}'

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValueError('Los movimientos del kardex no se pueden modificar.')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValueError('Los movimientos del kardex no se pueden eliminar.')