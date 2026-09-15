from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Categoria, Marca, UnidadMedida, Proveedor, Producto


class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto
        fields = (
            'sku', 'codigo_barras', 'nombre', 'marca', 'categoria',
            'precio_venta', 'stock_minimo', 'stock_maximo',
            'peso_kg', 'clasificacion_abc', 'activo'
        )
        export_order = fields


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais_origen', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(UnidadMedida)
class UnidadMedidaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'abreviatura', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'abreviatura')


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'numero_documento', 'telefono',
                    'email', 'ciudad', 'activo')
    list_filter = ('activo', 'ciudad', 'tipo_documento')
    search_fields = ('razon_social', 'nombre_comercial',
                     'numero_documento', 'email')


@admin.register(Producto)
class ProductoAdmin(ImportExportModelAdmin):
    resource_class = ProductoResource
    list_display = ('sku', 'codigo_barras', 'nombre', 'marca', 'categoria',
                    'precio_venta', 'stock_actual', 'bajo_stock',
                    'clasificacion_abc', 'activo')
    list_filter = ('marca', 'categoria', 'clasificacion_abc',
                   'activo', 'controla_imei')
    search_fields = ('sku', 'codigo_barras', 'nombre', 'especificaciones')
    list_select_related = ('marca', 'categoria')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    fieldsets = (
        ('Identificación', {
            'fields': ('sku', 'codigo_barras', 'nombre', 'marca', 'categoria')
        }),
        ('Clasificación', {
            'fields': ('unidad_medida', 'proveedor', 'clasificacion_abc')
        }),
        ('Especificaciones', {
            'fields': ('especificaciones', 'imagen', 'peso_kg', 'controla_imei')
        }),
        ('Inventario', {
            'fields': ('precio_venta', 'stock_minimo', 'stock_maximo')
        }),
        ('Estado', {
            'fields': ('activo', 'fecha_creacion', 'fecha_actualizacion')
        }),
    )

    @admin.display(description='Stock actual')
    def stock_actual(self, obj):
        return obj.stock_actual

    @admin.display(description='Bajo stock', boolean=True)
    def bajo_stock(self, obj):
        return obj.bajo_stock