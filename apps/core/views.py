from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone


@login_required
def home(request):
    from apps.catalogo.models import Producto
    from apps.almacen.models import Ubicacion
    from apps.inventario.models import Existencia, Movimiento

    total_productos = Producto.objects.filter(activo=True).count()
    total_ubicaciones = Ubicacion.objects.filter(activo=True).count()
    stock_total = Existencia.objects.aggregate(total=Sum('cantidad'))['total'] or 0
    bajo_stock = sum(1 for p in Producto.objects.filter(activo=True) if p.bajo_stock)
    movimientos_hoy = Movimiento.objects.filter(fecha__date=timezone.now().date()).count()

    ultimos_movimientos = Movimiento.objects.select_related(
        'producto', 'usuario', 'ubicacion_origen', 'ubicacion_destino'
    ).order_by('-fecha')[:5]

    context = {
        'total_productos': total_productos,
        'total_ubicaciones': total_ubicaciones,
        'stock_total': stock_total,
        'bajo_stock': bajo_stock,
        'movimientos_hoy': movimientos_hoy,
        'ultimos_movimientos': ultimos_movimientos,
    }

    return render(request, 'core/home.html', context)


def error_403(request, exception=None):
    """
    Vista personalizada para error 403 (Sin acceso).
    """
    return render(request, '403.html', status=403)