from django.contrib import admin
from .models import Existencia, Movimiento


@admin.register(Existencia)
class ExistenciaAdmin(admin.ModelAdmin):
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
class MovimientoAdmin(admin.ModelAdmin):
    """
    Kardex de SOLO LECTURA.
    No permite agregar, editar ni borrar desde el admin.
    Los movimientos se crean SOLO a través de services.py
    """
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