from django.contrib import admin
from .models import Bodega, Zona, Ubicacion, MovimientoUbicacion


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


class ZonaInline(admin.TabularInline):
    model = Zona
    extra = 0


@admin.register(Bodega)
class BodegaAdmin(ModuloAdminMixin, admin.ModelAdmin):
    modulo = 'Almacen'
    list_display = ('codigo', 'nombre', 'ciudad', 'activo')
    list_filter = ('activo', 'ciudad')
    search_fields = ('codigo', 'nombre', 'direccion')
    inlines = [ZonaInline]


class UbicacionInline(admin.TabularInline):
    model = Ubicacion
    extra = 0


@admin.register(Zona)
class ZonaAdmin(ModuloAdminMixin, admin.ModelAdmin):
    modulo = 'Almacen'
    list_display = ('codigo', 'nombre', 'bodega', 'tipo', 'activo')
    list_filter = ('bodega', 'tipo', 'activo')
    search_fields = ('codigo', 'nombre')
    list_select_related = ('bodega',)
    inlines = [UbicacionInline]


@admin.register(Ubicacion)
class UbicacionAdmin(ModuloAdminMixin, admin.ModelAdmin):
    modulo = 'Almacen'
    list_display = ('codigo', 'zona', 'tipo_ubicacion', 'capacidad_maxima',
                    'ocupacion_actual', 'porcentaje_ocupacion', 'activo')
    list_filter = ('zona__bodega', 'zona', 'tipo_ubicacion', 'activo')
    search_fields = ('codigo', 'pasillo', 'rack', 'nivel')
    list_select_related = ('zona', 'zona__bodega')
    readonly_fields = ('ocupacion_actual', 'porcentaje_ocupacion')


@admin.register(MovimientoUbicacion)
class MovimientoUbicacionAdmin(ModuloAdminMixin, admin.ModelAdmin):
    modulo = 'Almacen'
    list_display = ('fecha', 'tipo', 'ubicacion', 'producto', 'cantidad', 'usuario')
    list_filter = ('tipo', 'fecha', 'ubicacion__zona__bodega')
    search_fields = ('producto__sku', 'ubicacion__codigo')
    list_select_related = ('ubicacion', 'producto', 'usuario')
    readonly_fields = ('fecha',)