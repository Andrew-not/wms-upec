"""
Dashboard personalizado para Unfold.
Muestra los KPIs del WMS TechStock.
"""
from django.utils.translation import gettext_lazy as _


def dashboard_callback(request, context):
    """
    Callback que se ejecuta al cargar el admin.
    Añade los KPIs al contexto.
    """
    from apps.catalogo.models import Producto
    from apps.almacen.models import Ubicacion
    from apps.inventario.models import Existencia, Movimiento
    from django.db.models import Sum, Count
    from django.utils import timezone
    from datetime import timedelta

    # KPIs
    total_productos = Producto.objects.filter(activo=True).count()
    total_ubicaciones = Ubicacion.objects.filter(activo=True).count()
    
    stock_total = Existencia.objects.aggregate(
        total=Sum('cantidad')
    )['total'] or 0
    
    bajo_stock = sum(
        1 for p in Producto.objects.filter(activo=True)
        if p.bajo_stock
    )
    
    movimientos_hoy = Movimiento.objects.filter(
        fecha__date=timezone.now().date()
    ).count()
    
    # Últimos 5 movimientos
    ultimos_movimientos = Movimiento.objects.select_related(
        'producto', 'usuario', 'ubicacion_origen', 'ubicacion_destino'
    ).order_by('-fecha')[:5]
    
    context.update({
        'kpi_productos': total_productos,
        'kpi_ubicaciones': total_ubicaciones,
        'kpi_stock_total': stock_total,
        'kpi_bajo_stock': bajo_stock,
        'kpi_movimientos_hoy': movimientos_hoy,
        'ultimos_movimientos': ultimos_movimientos,
    })
    
    return context