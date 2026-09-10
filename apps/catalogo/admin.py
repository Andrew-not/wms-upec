from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Categoria, Marca, Producto


class ProductoResource(resources.ModelResource):
    class Meta:
        model = Producto
        fields = ('sku', 'nombre', 'marca', 'categoria',
                  'precio_venta', 'stock_minimo', 'stock_maximo', 'activo')


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


@admin.register(Producto)
class ProductoAdmin(ImportExportModelAdmin):
    resource_class = ProductoResource
    list_display = ('sku', 'nombre', 'marca', 'categoria',
                    'precio_venta', 'stock_actual', 'bajo_stock', 'activo')
    list_filter = ('marca', 'categoria', 'activo', 'controla_imei')
    search_fields = ('sku', 'nombre', 'especificaciones')
    list_select_related = ('marca', 'categoria')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    fieldsets = (
        ('Identificación', {
            'fields': ('sku', 'nombre', 'marca', 'categoria')
        }),
        ('Especificaciones', {
            'fields': ('especificaciones', 'controla_imei')
        }),
        ('Inventario', {
            'fields': ('precio_venta', 'stock_minimo', 'stock_maximo')
        }),
        ('Estado', {
            'fields': ('activo', 'fecha_creacion', 'fecha_actualizacion')
        }),
    )

    @admin.display(description='Stock actual', ordering='existencias__cantidad')
    def stock_actual(self, obj):
        return obj.stock_actual

    @admin.display(description='Bajo stock', boolean=True)
    def bajo_stock(self, obj):
        return obj.bajo_stock