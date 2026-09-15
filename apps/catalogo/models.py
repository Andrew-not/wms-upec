from django.db import models
from django.core.validators import MinValueValidator


class Categoria(models.Model):
    """
    Clasificación de productos tecnológicos.
    """
    nombre = models.CharField('Nombre', max_length=100, unique=True)
    descripcion = models.TextField('Descripción', blank=True)
    activo = models.BooleanField('Activo', default=True)
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Marca(models.Model):
    """
    Fabricante del dispositivo.
    """
    nombre = models.CharField('Nombre', max_length=100, unique=True)
    pais_origen = models.CharField('País de origen', max_length=100, blank=True)
    activo = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class UnidadMedida(models.Model):
    """
    Unidad de medida para los productos.
    """
    nombre = models.CharField('Nombre', max_length=50, unique=True)
    abreviatura = models.CharField(
        'Abreviatura',
        max_length=10,
        unique=True,
        help_text='Ej: UND, CJ, PACK'
    )
    activo = models.BooleanField('Activo', default=True)

    class Meta:
        verbose_name = 'Unidad de medida'
        verbose_name_plural = 'Unidades de medida'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.abreviatura})'


class Proveedor(models.Model):
    """
    Proveedor o distribuidor de los productos.
    """
    TIPOS_DOCUMENTO = (
        ('RUC', 'RUC'),
        ('CED', 'Cédula'),
        ('PAS', 'Pasaporte'),
    )

    tipo_documento = models.CharField(
        'Tipo de documento',
        max_length=3,
        choices=TIPOS_DOCUMENTO,
        default='RUC'
    )
    numero_documento = models.CharField(
        'Número de documento',
        max_length=20,
        unique=True
    )
    razon_social = models.CharField('Razón social', max_length=200)
    nombre_comercial = models.CharField('Nombre comercial', max_length=200, blank=True)
    contacto = models.CharField('Persona de contacto', max_length=150, blank=True)
    telefono = models.CharField('Teléfono', max_length=20, blank=True)
    email = models.EmailField('Email', blank=True)
    direccion = models.CharField('Dirección', max_length=300, blank=True)
    ciudad = models.CharField('Ciudad', max_length=100, blank=True)
    pais = models.CharField('País', max_length=100, default='Ecuador')
    activo = models.BooleanField('Activo', default=True)
    fecha_registro = models.DateTimeField('Fecha de registro', auto_now_add=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['razon_social']

    def __str__(self):
        return f'{self.razon_social} ({self.numero_documento})'


class Producto(models.Model):
    """
    Modelo de dispositivo. Representa el SKU del catálogo.
    """
    sku = models.CharField(
        'SKU',
        max_length=50,
        unique=True,
        help_text='Código único del producto. Ej: APL-IP15-128'
    )
    codigo_barras = models.CharField(
        'Código de barras',
        max_length=50,
        blank=True,
        db_index=True,
        help_text='EAN-13, UPC, etc.'
    )
    nombre = models.CharField('Nombre del modelo', max_length=200)
    marca = models.ForeignKey(
        Marca,
        on_delete=models.PROTECT,
        related_name='productos',
        verbose_name='Marca'
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
        verbose_name='Categoría'
    )
    unidad_medida = models.ForeignKey(
        UnidadMedida,
        on_delete=models.PROTECT,
        related_name='productos',
        verbose_name='Unidad de medida',
        null=True,
        blank=True
    )
    proveedor = models.ForeignKey(
        Proveedor,
        on_delete=models.PROTECT,
        related_name='productos',
        verbose_name='Proveedor principal',
        null=True,
        blank=True
    )
    especificaciones = models.TextField(
        'Especificaciones técnicas',
        blank=True,
        help_text='RAM, almacenamiento, procesador, pantalla, batería, SO'
    )
    imagen = models.ImageField(
        'Imagen del producto',
        upload_to='productos/',
        blank=True,
        null=True
    )
    peso_kg = models.DecimalField(
        'Peso (kg)',
        max_digits=6,
        decimal_places=3,
        default=0,
        validators=[MinValueValidator(0)]
    )
    precio_venta = models.DecimalField(
        'Precio de venta',
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        default=0
    )
    stock_minimo = models.PositiveIntegerField(
        'Stock mínimo',
        default=5,
        help_text='Cantidad mínima antes de generar alerta'
    )
    stock_maximo = models.PositiveIntegerField(
        'Stock máximo',
        default=100
    )
    clasificacion_abc = models.CharField(
        'Clasificación ABC',
        max_length=1,
        choices=[
            ('A', 'A - Alta rotación'),
            ('B', 'B - Media rotación'),
            ('C', 'C - Baja rotación'),
        ],
        default='C'
    )
    controla_imei = models.BooleanField(
        'Controla IMEI/Serial',
        default=True,
        help_text='Si es True, cada unidad se rastrea individualmente'
    )
    activo = models.BooleanField('Activo', default=True)
    fecha_creacion = models.DateTimeField('Fecha de creación', auto_now_add=True)
    fecha_actualizacion = models.DateTimeField('Última actualización', auto_now=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['marca__nombre', 'nombre']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['codigo_barras']),
            models.Index(fields=['marca', 'categoria']),
        ]

    def __str__(self):
        return f'{self.sku} - {self.marca.nombre} {self.nombre}'

    @property
    def stock_actual(self):
        from django.db.models import Sum
        total = self.existencias.aggregate(total=Sum('cantidad'))['total']
        return total or 0

    @property
    def bajo_stock(self):
        return self.stock_actual < self.stock_minimo