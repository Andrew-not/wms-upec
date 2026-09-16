from django.contrib import admin
from .models import (
    TareaPersonal, EventoCalendario, NotaRapida,
    Notificacion, Meta, PreferenciaUsuario, ActividadReciente
)


@admin.register(TareaPersonal)
class TareaPersonalAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'categoria', 'prioridad', 'estado', 'fecha_limite')
    list_filter = ('estado', 'prioridad', 'categoria')
    search_fields = ('titulo', 'descripcion')
    date_hierarchy = 'fecha_creacion'


@admin.register(EventoCalendario)
class EventoCalendarioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'tipo', 'fecha_inicio', 'fecha_fin', 'completado')
    list_filter = ('tipo', 'completado')
    search_fields = ('titulo', 'descripcion')
    date_hierarchy = 'fecha_inicio'


@admin.register(NotaRapida)
class NotaRapidaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'color', 'fijada', 'fecha_actualizacion')
    list_filter = ('color', 'fijada')
    search_fields = ('titulo', 'contenido')


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'destinatario', 'tipo', 'leida', 'fecha_creacion')
    list_filter = ('tipo', 'leida')
    search_fields = ('titulo', 'mensaje')
    date_hierarchy = 'fecha_creacion'


@admin.register(Meta)
class MetaAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'usuario', 'tipo', 'objetivo', 'progreso', 'periodo', 'activa')
    list_filter = ('tipo', 'periodo', 'activa')
    search_fields = ('descripcion',)


@admin.register(PreferenciaUsuario)
class PreferenciaUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tema', 'notif_email', 'notif_dashboard')
    search_fields = ('usuario__username',)


@admin.register(ActividadReciente)
class ActividadRecienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'modulo', 'descripcion', 'fecha')
    list_filter = ('accion', 'modulo')
    search_fields = ('descripcion',)
    date_hierarchy = 'fecha'