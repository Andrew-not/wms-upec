from django.contrib import admin
from .models import OrdenRecepcion, LineaRecepcion


class LineaRecepcionInline(admin.TabularInline):
    model = LineaRecepcion
    extra = 0
    readonly_fields = ('cantidad_recibida', 'fecha_recepcion')


@admin.register(OrdenRecepcion)
class OrdenRecepcionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'proveedor', 'fecha_esperada', 'estado',
                    'total_lineas', 'porcentaje_recepcion')
    list_filter = ('estado', 'proveedor', 'fecha_esperada')
    search_fields = ('numero', 'documento_referencia')
    date_hierarchy = 'fecha_creacion'
    inlines = [LineaRecepcionInline]
    readonly_fields = ('fecha_creacion', 'fecha_recepcion')
    list_select_related = ('proveedor',)


@admin.register(LineaRecepcion)
class LineaRecepcionAdmin(admin.ModelAdmin):
    list_display = ('orden', 'producto', 'cantidad_esperada',
                    'cantidad_recibida', 'ubicacion_destino')
    list_filter = ('orden__estado',)
    search_fields = ('orden__numero', 'producto__sku')
    list_select_related = ('orden', 'producto', 'ubicacion_destino')