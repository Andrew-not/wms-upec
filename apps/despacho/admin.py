from django.contrib import admin
from .models import Cliente, Pedido, LineaPedido


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


@admin.register(Cliente)
class ClienteAdmin(ModuloAdminMixin, admin.ModelAdmin):
    modulo = 'Despacho'
    list_display = ('razon_social', 'numero_documento', 'tipo_documento',
                    'email', 'telefono', 'ciudad', 'activo')
    list_filter = ('tipo_documento', 'ciudad', 'activo')
    search_fields = ('razon_social', 'numero_documento', 'email')
    ordering = ('razon_social',)


class LineaPedidoInline(admin.TabularInline):
    model = LineaPedido
    extra = 0
    readonly_fields = ('cantidad_preparada',)


@admin.register(Pedido)
class PedidoAdmin(ModuloAdminMixin, admin.ModelAdmin):
    modulo = 'Despacho'
    list_display = ('numero', 'cliente', 'prioridad', 'estado',
                    'fecha_pedido', 'fecha_entrega',
                    'total_lineas', 'porcentaje_preparacion')
    list_filter = ('estado', 'prioridad', 'fecha_pedido')
    search_fields = ('numero', 'cliente__razon_social')
    date_hierarchy = 'fecha_pedido'
    inlines = [LineaPedidoInline]
    readonly_fields = ('fecha_creacion', 'fecha_despacho')
    list_select_related = ('cliente',)


@admin.register(LineaPedido)
class LineaPedidoAdmin(ModuloAdminMixin, admin.ModelAdmin):
    modulo = 'Despacho'
    list_display = ('pedido', 'producto', 'cantidad', 'cantidad_preparada',
                    'precio_unitario', 'ubicacion_origen')
    list_filter = ('pedido__estado',)
    search_fields = ('pedido__numero', 'producto__sku')
    list_select_related = ('pedido', 'producto', 'ubicacion_origen')