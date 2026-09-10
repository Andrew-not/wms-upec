from django.contrib import admin
from .models import Bodega, Zona, Ubicacion


class ZonaInline(admin.TabularInline):
    model = Zona
    extra = 0


@admin.register(Bodega)
class BodegaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'ciudad', 'activo')
    list_filter = ('activo', 'ciudad')
    search_fields = ('codigo', 'nombre', 'direccion')
    inlines = [ZonaInline]


class UbicacionInline(admin.TabularInline):
    model = Ubicacion
    extra = 0


@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'bodega', 'tipo', 'activo')
    list_filter = ('bodega', 'tipo', 'activo')
    search_fields = ('codigo', 'nombre')
    list_select_related = ('bodega',)
    inlines = [UbicacionInline]


@admin.register(Ubicacion)
class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'zona', 'capacidad_maxima',
                    'ocupacion_actual', 'porcentaje_ocupacion', 'activo')
    list_filter = ('zona__bodega', 'zona', 'activo')
    search_fields = ('codigo', 'pasillo', 'rack', 'nivel')
    list_select_related = ('zona', 'zona__bodega')
    readonly_fields = ('ocupacion_actual', 'porcentaje_ocupacion')