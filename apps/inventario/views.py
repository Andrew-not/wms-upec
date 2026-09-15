from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


@login_required
def kardex(request):
    """
    Kardex de movimientos con filtros y paginación.
    Solo lectura: no permite editar ni eliminar.
    """
    from apps.inventario.models import Movimiento

    # Queryset base
    movimientos = Movimiento.objects.select_related(
        'producto', 'usuario', 'ubicacion_origen', 'ubicacion_destino'
    ).order_by('-fecha')

    # Filtros
    tipo = request.GET.get('tipo', '')
    producto_q = request.GET.get('producto', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    if tipo:
        movimientos = movimientos.filter(tipo=tipo)

    if producto_q:
        movimientos = movimientos.filter(
            Q(producto__sku__icontains=producto_q) |
            Q(producto__nombre__icontains=producto_q)
        )

    if fecha_desde:
        movimientos = movimientos.filter(fecha__date__gte=fecha_desde)

    if fecha_hasta:
        movimientos = movimientos.filter(fecha__date__lte=fecha_hasta)

    # Paginación
    paginator = Paginator(movimientos, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Opciones de tipos para el filtro
    tipos = Movimiento.TIPOS

    context = {
        'page_obj': page_obj,
        'tipos': tipos,
        'total_movimientos': movimientos.count(),
        'filtros': {
            'tipo': tipo,
            'producto': producto_q,
            'fecha_desde': fecha_desde,
            'fecha_hasta': fecha_hasta,
        }
    }

    return render(request, 'inventario/kardex.html', context)