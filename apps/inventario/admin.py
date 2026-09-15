from django.contrib import admin
from .models import Existencia, Movimiento


class ModuloAdminMixin:
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


@admin.register(Existencia)
class ExistenciaAdmin(ModuloAdminMixin, admin.ModelAdmin):
    modulo = 'Inventario'
    list_display = ('producto', 'ubicacion', 'cantidad',
                    'cantidad_reservada', 'cantidad_disponible', 'fecha_actualizacion')
    list_filter = ('ubicacion__zona__bodega', 'ubicacion__zona')
    search_fields = ('producto__sku', 'producto__nombre', 'ubicacion__codigo')
    list_select_related = ('producto', 'ubicacion')
    readonly_fields = ('fecha_actualizacion',)

    @admin.display(description='Disponible')
    def cantidad_disponible(self, obj):
        return obj.cantidad_disponible


@admin.register(Movimiento)
class MovimientoAdmin(ModuloAdminMixin, admin.ModelAdmin):
    """
    Kardex de SOLO LECTURA.
    """
    modulo = 'Inventario'
    list_display = ('fecha', 'tipo', 'producto', 'cantidad',
                    'ubicacion_origen', 'ubicacion_destino',
                    'usuario', 'documento')
    list_filter = ('tipo', 'fecha', 'usuario')
    search_fields = ('producto__sku', 'producto__nombre',
                     'documento', 'observacion')
    list_select_related = ('producto', 'ubicacion_origen',
                          'ubicacion_destino', 'usuario')
    date_hierarchy = 'fecha'
    readonly_fields = ('tipo', 'producto', 'cantidad',
                       'ubicacion_origen', 'ubicacion_destino',
                       'documento', 'observacion', 'usuario',
                       'fecha', 'fecha_movimiento')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False