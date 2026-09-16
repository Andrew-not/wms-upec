from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta


@login_required
def mi_espacio(request):
    """Dashboard personal del usuario."""
    from .models import (
        TareaPersonal, EventoCalendario, NotaRapida,
        Notificacion, Meta, ActividadReciente
    )

    usuario = request.user
    hoy = timezone.now()

    # Tareas del usuario
    tareas_pendientes = TareaPersonal.objects.filter(
        usuario=usuario,
        estado__in=['PENDIENTE', 'EN_PROCESO']
    ).order_by('-prioridad', 'fecha_limite')[:10]

    # Eventos próximos (próximos 7 días)
    eventos_proximos = EventoCalendario.objects.filter(
        usuario=usuario,
        fecha_inicio__gte=hoy,
        fecha_inicio__lte=hoy + timedelta(days=7),
        completado=False
    ).order_by('fecha_inicio')[:5]

    # Notas rápidas
    notas = NotaRapida.objects.filter(usuario=usuario)[:6]

    # Metas activas
    metas = Meta.objects.filter(usuario=usuario, activa=True)[:5]

    # Notificaciones no leídas
    notificaciones_no_leidas = Notificacion.objects.filter(
        destinatario=usuario,
        leida=False
    ).order_by('-fecha_creacion')[:10]

    # Actividad reciente
    actividad = ActividadReciente.objects.filter(usuario=usuario)[:10]

    # KPIs personales
    total_tareas = TareaPersonal.objects.filter(usuario=usuario).count()
    tareas_completadas = TareaPersonal.objects.filter(
        usuario=usuario, estado='COMPLETADA'
    ).count()
    total_eventos = EventoCalendario.objects.filter(
        usuario=usuario, fecha_inicio__gte=hoy
    ).count()
    total_metas = Meta.objects.filter(usuario=usuario, activa=True).count()

    context = {
        'tareas_pendientes': tareas_pendientes,
        'eventos_proximos': eventos_proximos,
        'notas': notas,
        'metas': metas,
        'notificaciones': notificaciones_no_leidas,
        'actividad': actividad,
        'total_tareas': total_tareas,
        'tareas_completadas': tareas_completadas,
        'total_eventos': total_eventos,
        'total_metas': total_metas,
    }

    return render(request, 'workspace/mi_espacio.html', context)