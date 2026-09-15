from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class Cliente(models.Model):
    """
    Cliente que realiza pedidos.
    """
    TIPOS_DOCUMENTO = [
        ('CED', 'Cédula'),
        ('RUC', 'RUC'),
        ('PAS', 'Pasaporte'),
    ]

    tipo_documento = models.CharField(
        'Tipo de documento',
        max_length=3,
        choices=TIPOS_DOCUMENTO,
        default='CED'
    )
    numero_documento = models.CharField(
        'Número de documento',
        max_length=20,
        unique=True
    )
    razon_social = models.CharField('Razón social', max_length=200)
    email = models.EmailField('Email', blank=True)
    telefono = models.CharField('Teléfono', max_length=20, blank=True)
    direccion = models.CharField('Dirección', max_length=300, blank=True)
    ciudad = models.CharField('Ciudad', max_length=100, blank=True)
    activo = models.BooleanField('Activo', default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['razon_social']

    def __str__(self):
        return f'{self.razon_social} ({self.numero_documento})'


class Pedido(models.Model):
    """
    Pedido de venta a un cliente.
    """
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('PICKING', 'En picking'),
        ('PREPARADO', 'Preparado'),
        ('DESPACHADO', 'Despachado'),
        ('CANCELADO', 'Cancelado'),
    ]
    PRIORIDADES = [
        ('BAJA', 'Baja'),
        ('NORMAL', 'Normal'),
        ('ALTA', 'Alta'),
        ('URGENTE', 'Urgente'),
    ]

    numero = models.CharField(
        'Número de pedido',
        max_length=20,
        unique=True,
        help_text='Ej: PED-2026-001'
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name='pedidos',
        verbose_name='Cliente'
    )
    fecha_pedido = models.DateField('Fecha de pedido', auto_now_add=True)
    fecha_entrega = models.DateField('Fecha de entrega estimada')
    fecha_despacho = models.DateField('Fecha de despacho', null=True, blank=True)
    prioridad = models.CharField(
        'Prioridad',
        max_length=10,
        choices=PRIORIDADES,
        default='NORMAL'
    )
    estado = models.CharField(
        'Estado',
        max_length=15,
        choices=ESTADOS,
        default='PENDIENTE'
    )
    direccion_entrega = models.CharField('Dirección de entrega', max_length=300, blank=True)
    observaciones = models.TextField('Observaciones', blank=True)
    usuario_creacion = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='pedidos_creados',
        verbose_name='Usuario creador'
    )
    usuario_despacho = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='pedidos_despachados',
        verbose_name='Usuario que despachó',
        null=True,
        blank=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.numero} - {self.cliente.razon_social}'

    @property
    def total_lineas(self):
        return self.lineas.count()

    @property
    def total_unidades(self):
        return sum(l.cantidad for l in self.lineas.all())

    @property
    def total_pedido(self):
        return sum(l.subtotal for l in self.lineas.all())

    @property
    def porcentaje_preparacion(self):
        total = self.total_unidades
        if total == 0:
            return 0
        preparado = sum(l.cantidad_preparada for l in self.lineas.all())
        return round((preparado / total) * 100, 1)


class LineaPedido(models.Model):
    """
    Línea individual de un pedido.
    """
    pedido = models.ForeignKey(
        Pedido,
        on_delete=models.CASCADE,
        related_name='lineas',
        verbose_name='Pedido'
    )
    producto = models.ForeignKey(
        'catalogo.Producto',
        on_delete=models.PROTECT,
        related_name='lineas_pedido',
        verbose_name='Producto'
    )
    cantidad = models.IntegerField(
        'Cantidad',
        validators=[MinValueValidator(1)]
    )
    cantidad_preparada = models.IntegerField(
        'Cantidad preparada',
        default=0,
        validators=[MinValueValidator(0)]
    )
    precio_unitario = models.DecimalField(
        'Precio unitario',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    ubicacion_origen = models.ForeignKey(
        'almacen.Ubicacion',
        on_delete=models.PROTECT,
        related_name='pedidos',
        verbose_name='Ubicación origen',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Línea de pedido'
        verbose_name_plural = 'Líneas de pedido'
        unique_together = [['pedido', 'producto']]
        ordering = ['pedido', 'producto']

    def __str__(self):
        return f'{self.producto.sku} x {self.cantidad}'

    @property
    def subtotal(self):
        return Decimal(self.cantidad) * self.precio_unitario

    @property
    def completa(self):
        return self.cantidad_preparada >= self.cantidad