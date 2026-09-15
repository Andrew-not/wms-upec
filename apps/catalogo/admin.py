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


class ModuloAdminMixin:
    """
    Solo usuarios de este modulo (o superusuarios) pueden ver/modificar.
    """
    modulo = None

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name=f'Operario {self.modulo}').exists()

    def has_view_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_add_permission(self, request):
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Categoria)
class CategoriaAdmin(ModuloAdminMixin, admin.ModelAdmin):
    modulo = 'Catalogo'
    list_display = ('nombre', 'activo', 'fecha_creacion')
    list_filter = ('activo',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Marca)
class MarcaAdmin(ModuloAdminMixin, admin.ModelAdmin):
    modulo = 'Catalogo'
    list_display = ('nombre', 'pais_origen', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(UnidadMedida)
class UnidadMedidaAdmin(ModuloAdminMixin, admin.ModelAdmin):
    modulo = 'Catalogo'
    list_display = ('nombre', 'abreviatura', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre', 'abreviatura')


@admin.register(Proveedor)
class ProveedorAdmin(ModuloAdminMixin, admin.ModelAdmin):
    modulo = 'Catalogo'
    list_display = ('razon_social', 'numero_documento', 'telefono',
                    'email', 'ciudad', 'activo')
    list_filter = ('activo', 'ciudad', 'tipo_documento')
    search_fields = ('razon_social', 'nombre_comercial',
                     'numero_documento', 'email')


@admin.register(Producto)
class ProductoAdmin(ModuloAdminMixin, ImportExportModelAdmin):
    modulo = 'Catalogo'
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