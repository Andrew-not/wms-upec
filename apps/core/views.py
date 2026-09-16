from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
import json


@login_required
def home(request):
    from apps.catalogo.models import Producto, Categoria
    from apps.almacen.models import Ubicacion
    from apps.inventario.models import Existencia, Movimiento

    # KPIs
    total_productos = Producto.objects.filter(activo=True).count()
    total_ubicaciones = Ubicacion.objects.filter(activo=True).count()
    stock_total = Existencia.objects.aggregate(total=Sum('cantidad'))['total'] or 0
    bajo_stock = sum(1 for p in Producto.objects.filter(activo=True) if p.bajo_stock)
    movimientos_hoy = Movimiento.objects.filter(fecha__date=timezone.now().date()).count()

    # Últimos 5 movimientos
    ultimos_movimientos = Movimiento.objects.select_related(
        'producto', 'usuario', 'ubicacion_origen', 'ubicacion_destino'
    ).order_by('-fecha')[:5]

    # ==========================================
    # GRÁFICA 1: Movimientos últimos 30 días
    # ==========================================
    hoy = timezone.now().date()
    hace_30_dias = hoy - timedelta(days=30)

    labels_fechas = []
    entradas_data = []
    salidas_data = []

    for i in range(30):
        fecha = hace_30_dias + timedelta(days=i)
        labels_fechas.append(fecha.strftime('%d/%m'))
        entradas_data.append(
            Movimiento.objects.filter(fecha__date=fecha, tipo='ENTRADA').count()
        )
        salidas_data.append(
            Movimiento.objects.filter(fecha__date=fecha, tipo='SALIDA').count()
        )

    # ==========================================
    # GRÁFICA 2: Stock por categoría
    # ==========================================
    categorias = Categoria.objects.filter(activo=True)
    labels_categorias = []
    stock_categorias = []

    for cat in categorias:
        labels_categorias.append(cat.nombre)
        total = Existencia.objects.filter(
            producto__categoria=cat
        ).aggregate(total=Sum('cantidad'))['total'] or 0
        stock_categorias.append(total)

    # ==========================================
    # GRÁFICA 3: Ocupación por bodega
    # ==========================================
    from apps.almacen.models import Bodega
    bodegas = Bodega.objects.filter(activo=True)
    labels_bodegas = []
    ocupacion_bodegas = []

    for bod in bodegas:
        labels_bodegas.append(bod.nombre)
        total = Existencia.objects.filter(
            ubicacion__zona__bodega=bod
        ).aggregate(total=Sum('cantidad'))['total'] or 0
        ocupacion_bodegas.append(total)

    context = {
        'total_productos': total_productos,
        'total_ubicaciones': total_ubicaciones,
        'stock_total': stock_total,
        'bajo_stock': bajo_stock,
        'movimientos_hoy': movimientos_hoy,
        'ultimos_movimientos': ultimos_movimientos,
        # Datos para gráficas
        'fechas_json': json.dumps(labels_fechas),
        'entradas_json': json.dumps(entradas_data),
        'salidas_json': json.dumps(salidas_data),
        'categorias_json': json.dumps(labels_categorias),
        'stock_categorias_json': json.dumps(stock_categorias),
        'bodegas_json': json.dumps(labels_bodegas),
        'ocupacion_bodegas_json': json.dumps(ocupacion_bodegas),
    }

    return render(request, 'core/home.html', context)


def error_403(request, exception=None):
    return render(request, '403.html', status=403)