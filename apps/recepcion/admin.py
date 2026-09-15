from django.contrib import admin
from .models import OrdenRecepcion, LineaRecepcion


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


class LineaRecepcionInline(admin.TabularInline):
    model = LineaRecepcion
    extra = 0
    readonly_fields = ('cantidad_recibida', 'fecha_recepcion')


@admin.register(OrdenRecepcion)
class OrdenRecepcionAdmin(ModuloAdminMixin, admin.ModelAdmin):
    modulo = 'Recepcion'
    list_display = ('numero', 'proveedor', 'fecha_esperada', 'estado',
                    'total_lineas', 'porcentaje_recepcion')
    list_filter = ('estado', 'proveedor', 'fecha_esperada')
    search_fields = ('numero', 'documento_referencia')
    date_hierarchy = 'fecha_creacion'
    inlines = [LineaRecepcionInline]
    readonly_fields = ('fecha_creacion', 'fecha_recepcion')
    list_select_related = ('proveedor',)


@admin.register(LineaRecepcion)
class LineaRecepcionAdmin(ModuloAdminMixin, admin.ModelAdmin):
    modulo = 'Recepcion'
    list_display = ('orden', 'producto', 'cantidad_esperada',
                    'cantidad_recibida', 'ubicacion_destino')
    list_filter = ('orden__estado',)
    search_fields = ('orden__numero', 'producto__sku')
    list_select_related = ('orden', 'producto', 'ubicacion_destino')