from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q


@login_required
def pedido_lista(request):
    """
    Listado de pedidos.
    """
    from apps.despacho.models import Pedido

    pedidos = Pedido.objects.select_related('cliente').order_by('-fecha_creacion')

    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '')
    prioridad = request.GET.get('prioridad', '')

    if q:
        pedidos = pedidos.filter(
            Q(numero__icontains=q) |
            Q(cliente__razon_social__icontains=q)
        )

    if estado:
        pedidos = pedidos.filter(estado=estado)

    if prioridad:
        pedidos = pedidos.filter(prioridad=prioridad)

    paginator = Paginator(pedidos, 15)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    total_pendientes = Pedido.objects.filter(estado='PENDIENTE').count()
    total_picking = Pedido.objects.filter(estado='PICKING').count()
    total_despachados = Pedido.objects.filter(estado='DESPACHADO').count()

    context = {
        'page_obj': page_obj,
        'total_pendientes': total_pendientes,
        'total_picking': total_picking,
        'total_despachados': total_despachados,
        'filtros': {'q': q, 'estado': estado, 'prioridad': prioridad},
    }

    return render(request, 'despacho/pedido_lista.html', context)


@login_required
def pedido_detalle(request, numero):
    """
    Detalle de un pedido.
    """
    from apps.despacho.models import Pedido

    pedido = get_object_or_404(Pedido, numero=numero)
    lineas = pedido.lineas.select_related('producto', 'ubicacion_origen')

    context = {
        'pedido': pedido,
        'lineas': lineas,
    }

    return render(request, 'despacho/pedido_detalle.html', context)


@login_required
def procesar_picking_view(request, numero):
    """
    Procesa el picking de un pedido.
    """
    from apps.despacho.models import Pedido
    from apps.despacho.services import procesar_picking, despachar_pedido
    from django.core.exceptions import ValidationError
    from apps.inventario.services import StockInsuficienteError

    pedido = get_object_or_404(Pedido, numero=numero)

    if request.method == 'POST':
        accion = request.POST.get('accion', 'picking')

        try:
            if accion == 'picking':
                procesar_picking(pedido, request.user, 'Picking procesado')
                messages.success(request, f'Picking del pedido {pedido.numero} completado.')
            elif accion == 'despachar':
                despachar_pedido(pedido, request.user, 'Pedido despachado')
                messages.success(request, f'Pedido {pedido.numero} despachado.')
        except StockInsuficienteError as e:
            messages.error(request, f'Stock insuficiente: {e}')
        except ValidationError as e:
            messages.error(request, f'Error: {e}')
        except Exception as e:
            messages.error(request, f'Error inesperado: {e}')

    return redirect('despacho:pedido_detalle', numero=pedido.numero)