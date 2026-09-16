from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta


@login_required
def mi_espacio(request):
    """Dashboard personal del usuario."""
    from .models import (
        TareaPersonal, EventoCalendario, NotaRapida,
        Notificacion, Meta, ActividadReciente, Mensaje
    )

    usuario = request.user
    hoy = timezone.now()

    tareas_pendientes = TareaPersonal.objects.filter(
        usuario=usuario, estado__in=['PENDIENTE', 'EN_PROCESO']
    ).order_by('-prioridad', 'fecha_limite')[:10]

    eventos_proximos = EventoCalendario.objects.filter(
        usuario=usuario, fecha_inicio__gte=hoy,
        fecha_inicio__lte=hoy + timedelta(days=7),
        completado=False
    ).order_by('fecha_inicio')[:5]

    notas = NotaRapida.objects.filter(usuario=usuario)[:6]
    metas = Meta.objects.filter(usuario=usuario, activa=True)[:5]
    
    notificaciones = Notificacion.objects.filter(
        destinatario=usuario, leida=False
    ).order_by('-fecha_creacion')[:10]

    mensajes_no_leidos = Mensaje.objects.filter(
        destinatario=usuario, leido=False
    ).order_by('-fecha_envio')[:5]

    actividad = ActividadReciente.objects.filter(usuario=usuario)[:10]

    context = {
        'tareas_pendientes': tareas_pendientes,
        'eventos_proximos': eventos_proximos,
        'notas': notas,
        'metas': metas,
        'notificaciones': notificaciones,
        'mensajes_no_leidos': mensajes_no_leidos,
        'actividad': actividad,
        'total_tareas': TareaPersonal.objects.filter(usuario=usuario).count(),
        'tareas_completadas': TareaPersonal.objects.filter(usuario=usuario, estado='COMPLETADA').count(),
        'total_eventos': EventoCalendario.objects.filter(usuario=usuario, fecha_inicio__gte=hoy).count(),
        'total_metas': Meta.objects.filter(usuario=usuario, activa=True).count(),
        'total_mensajes': Mensaje.objects.filter(destinatario=usuario, leido=False).count(),
    }
    return render(request, 'workspace/mi_espacio.html', context)


# ==========================================
# TAREAS
# ==========================================
@login_required
def tarea_lista(request):
    from .models import TareaPersonal
    tareas = TareaPersonal.objects.filter(usuario=request.user).order_by('estado', '-prioridad')
    return render(request, 'workspace/tarea_lista.html', {'tareas': tareas})


@login_required
def tarea_crear(request):
    from .forms import TareaForm
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.usuario = request.user
            tarea.save()
            messages.success(request, 'Tarea creada correctamente')
            return redirect('workspace:tarea_lista')
    else:
        form = TareaForm()
    return render(request, 'workspace/tarea_form.html', {'form': form, 'accion': 'Crear'})


@login_required
def tarea_editar(request, pk):
    from .forms import TareaForm
    from .models import TareaPersonal
    tarea = get_object_or_404(TareaPersonal, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea actualizada')
            return redirect('workspace:tarea_lista')
    else:
        form = TareaForm(instance=tarea)
    return render(request, 'workspace/tarea_form.html', {'form': form, 'accion': 'Editar'})


@login_required
def tarea_completar(request, pk):
    from .models import TareaPersonal
    tarea = get_object_or_404(TareaPersonal, pk=pk, usuario=request.user)
    tarea.estado = 'COMPLETADA'
    tarea.fecha_completada = timezone.now()
    tarea.save()
    messages.success(request, 'Tarea completada')
    return redirect('workspace:tarea_lista')


@login_required
def tarea_eliminar(request, pk):
    from .models import TareaPersonal
    tarea = get_object_or_404(TareaPersonal, pk=pk, usuario=request.user)
    tarea.delete()
    messages.success(request, 'Tarea eliminada')
    return redirect('workspace:tarea_lista')


# ==========================================
# EVENTOS
# ==========================================
@login_required
def evento_lista(request):
    from .models import EventoCalendario
    eventos = EventoCalendario.objects.filter(usuario=request.user).order_by('fecha_inicio')
    return render(request, 'workspace/evento_lista.html', {'eventos': eventos})


@login_required
def evento_crear(request):
    from .forms import EventoForm
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.usuario = request.user
            evento.save()
            messages.success(request, 'Evento creado correctamente')
            return redirect('workspace:evento_lista')
    else:
        form = EventoForm()
    return render(request, 'workspace/evento_form.html', {'form': form, 'accion': 'Crear'})


@login_required
def evento_editar(request, pk):
    from .forms import EventoForm
    from .models import EventoCalendario
    evento = get_object_or_404(EventoCalendario, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Evento actualizado')
            return redirect('workspace:evento_lista')
    else:
        form = EventoForm(instance=evento)
    return render(request, 'workspace/evento_form.html', {'form': form, 'accion': 'Editar'})


@login_required
def evento_eliminar(request, pk):
    from .models import EventoCalendario
    evento = get_object_or_404(EventoCalendario, pk=pk, usuario=request.user)
    evento.delete()
    messages.success(request, 'Evento eliminado')
    return redirect('workspace:evento_lista')


# ==========================================
# NOTAS
# ==========================================
@login_required
def nota_lista(request):
    from .models import NotaRapida
    notas = NotaRapida.objects.filter(usuario=request.user).order_by('-fijada', '-fecha_actualizacion')
    return render(request, 'workspace/nota_lista.html', {'notas': notas})


@login_required
def nota_crear(request):
    from .forms import NotaForm
    if request.method == 'POST':
        form = NotaForm(request.POST)
        if form.is_valid():
            nota = form.save(commit=False)
            nota.usuario = request.user
            nota.save()
            messages.success(request, 'Nota creada')
            return redirect('workspace:nota_lista')
    else:
        form = NotaForm()
    return render(request, 'workspace/nota_form.html', {'form': form, 'accion': 'Crear'})


@login_required
def nota_editar(request, pk):
    from .forms import NotaForm
    from .models import NotaRapida
    nota = get_object_or_404(NotaRapida, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = NotaForm(request.POST, instance=nota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nota actualizada')
            return redirect('workspace:nota_lista')
    else:
        form = NotaForm(instance=nota)
    return render(request, 'workspace/nota_form.html', {'form': form, 'accion': 'Editar'})


@login_required
def nota_eliminar(request, pk):
    from .models import NotaRapida
    nota = get_object_or_404(NotaRapida, pk=pk, usuario=request.user)
    nota.delete()
    messages.success(request, 'Nota eliminada')
    return redirect('workspace:nota_lista')


# ==========================================
# METAS
# ==========================================
@login_required
def meta_lista(request):
    from .models import Meta
    metas = Meta.objects.filter(usuario=request.user).order_by('-activa', 'fecha_fin')
    return render(request, 'workspace/meta_lista.html', {'metas': metas})


@login_required
def meta_crear(request):
    from .forms import MetaForm
    if request.method == 'POST':
        form = MetaForm(request.POST)
        if form.is_valid():
            meta = form.save(commit=False)
            meta.usuario = request.user
            meta.save()
            messages.success(request, 'Meta creada')
            return redirect('workspace:meta_lista')
    else:
        form = MetaForm()
    return render(request, 'workspace/meta_form.html', {'form': form, 'accion': 'Crear'})


@login_required
def meta_editar(request, pk):
    from .forms import MetaForm
    from .models import Meta
    meta = get_object_or_404(Meta, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = MetaForm(request.POST, instance=meta)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meta actualizada')
            return redirect('workspace:meta_lista')
    else:
        form = MetaForm(instance=meta)
    return render(request, 'workspace/meta_form.html', {'form': form, 'accion': 'Editar'})


@login_required
def meta_eliminar(request, pk):
    from .models import Meta
    meta = get_object_or_404(Meta, pk=pk, usuario=request.user)
    meta.delete()
    messages.success(request, 'Meta eliminada')
    return redirect('workspace:meta_lista')


# ==========================================
# MENSAJES
# ==========================================
@login_required
def mensaje_lista(request):
    from .models import Mensaje
    recibidos = Mensaje.objects.filter(destinatario=request.user).order_by('-fecha_envio')
    enviados = Mensaje.objects.filter(remitente=request.user).order_by('-fecha_envio')
    return render(request, 'workspace/mensaje_lista.html', {
        'recibidos': recibidos,
        'enviados': enviados,
    })


@login_required
def mensaje_crear(request):
    from .forms import MensajeForm
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.remitente = request.user
            mensaje.save()
            
            # Crear notificación automática
            from .models import Notificacion
            Notificacion.objects.create(
                destinatario=mensaje.destinatario,
                tipo='INFO',
                titulo=f'Nuevo mensaje de {request.user.username}',
                mensaje=mensaje.asunto,
                url_destino='/mi-espacio/mensajes/'
            )
            
            messages.success(request, 'Mensaje enviado')
            return redirect('workspace:mensaje_lista')
    else:
        form = MensajeForm()
    return render(request, 'workspace/mensaje_form.html', {'form': form, 'accion': 'Enviar'})


@login_required
def mensaje_ver(request, pk):
    from .models import Mensaje
    mensaje = get_object_or_404(Mensaje, pk=pk)
    
    if mensaje.destinatario != request.user and mensaje.remitente != request.user:
        messages.error(request, 'No tienes permiso para ver este mensaje')
        return redirect('workspace:mensaje_lista')
    
    if mensaje.destinatario == request.user and not mensaje.leido:
        mensaje.leido = True
        mensaje.fecha_lectura = timezone.now()
        mensaje.save()
    
    return render(request, 'workspace/mensaje_ver.html', {'mensaje': mensaje})


# ==========================================
# NOTIFICACIONES
# ==========================================
@login_required
def notificacion_lista(request):
    from .models import Notificacion
    notificaciones = Notificacion.objects.filter(
        destinatario=request.user
    ).order_by('-fecha_creacion')
    return render(request, 'workspace/notificacion_lista.html', {'notificaciones': notificaciones})


@login_required
def notificacion_marcar_leida(request, pk):
    from .models import Notificacion
    notif = get_object_or_404(Notificacion, pk=pk, destinatario=request.user)
    notif.leida = True
    notif.fecha_lectura = timezone.now()
    notif.save()
    return redirect('workspace:notificacion_lista')


@login_required
def notificacion_marcar_todas_leidas(request):
    from .models import Notificacion
    Notificacion.objects.filter(
        destinatario=request.user, leida=False
    ).update(leida=True, fecha_lectura=timezone.now())
    messages.success(request, 'Todas las notificaciones marcadas como leídas')
    return redirect('workspace:notificacion_lista')