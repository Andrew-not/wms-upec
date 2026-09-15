from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


@login_required
def orden_lista(request):
    """
    Listado de órdenes de recepción.
    """
    from apps.recepcion.models import OrdenRecepcion

    ordenes = OrdenRecepcion.objects.select_related('proveedor').order_by('-fecha_creacion')

    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '')

    if q:
        ordenes = ordenes.filter(
            Q(numero__icontains=q) |
            Q(proveedor__razon_social__icontains=q) |
            Q(documento_referencia__icontains=q)
        )

    if estado:
        ordenes = ordenes.filter(estado=estado)

    paginator = Paginator(ordenes, 15)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    total_pendientes = OrdenRecepcion.objects.filter(estado='PENDIENTE').count()
    total_en_proceso = OrdenRecepcion.objects.filter(estado='EN_PROCESO').count()
    total_recibidas = OrdenRecepcion.objects.filter(estado='RECIBIDA').count()

    context = {
        'page_obj': page_obj,
        'total_pendientes': total_pendientes,
        'total_en_proceso': total_en_proceso,
        'total_recibidas': total_recibidas,
        'filtros': {'q': q, 'estado': estado},
    }

    return render(request, 'recepcion/orden_lista.html', context)


@login_required
def orden_detalle(request, numero):
    """
    Detalle de una orden de recepción.
    """
    from apps.recepcion.models import OrdenRecepcion

    orden = get_object_or_404(OrdenRecepcion, numero=numero)
    lineas = orden.lineas.select_related('producto', 'ubicacion_destino')

    context = {
        'orden': orden,
        'lineas': lineas,
    }

    return render(request, 'recepcion/orden_detalle.html', context)


@login_required
def recibir_orden(request, numero):
    """
    Recibe completamente una orden pendiente.
    """
    from apps.recepcion.models import OrdenRecepcion
    from apps.recepcion.services import recibir_orden_completa
    from django.core.exceptions import ValidationError

    orden = get_object_or_404(OrdenRecepcion, numero=numero)

    if request.method == 'POST':
        try:
            recibir_orden_completa(orden, request.user, 'Recepción completa')
            messages.success(request, f'Orden {orden.numero} recibida correctamente.')
        except ValidationError as e:
            messages.error(request, f'Error: {e}')
        except Exception as e:
            messages.error(request, f'Error inesperado: {e}')

        return redirect('recepcion:orden_detalle', numero=orden.numero)

    return redirect('recepcion:orden_detalle', numero=orden.numero)