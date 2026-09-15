from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, Q


@login_required
def ubicacion_lista(request):
    """
    Listado de ubicaciones con barras de ocupación.
    """
    from apps.almacen.models import Ubicacion, Zona, Bodega

    ubicaciones = Ubicacion.objects.filter(activo=True).select_related(
        'zona', 'zona__bodega'
    ).order_by('codigo')

    q = request.GET.get('q', '').strip()
    bodega_id = request.GET.get('bodega', '')
    zona_id = request.GET.get('zona', '')
    estado = request.GET.get('estado', '')

    if q:
        ubicaciones = ubicaciones.filter(
            Q(codigo__icontains=q) |
            Q(pasillo__icontains=q) |
            Q(rack__icontains=q) |
            Q(nivel__icontains=q)
        )

    if bodega_id:
        ubicaciones = ubicaciones.filter(zona__bodega_id=bodega_id)

    if zona_id:
        ubicaciones = ubicaciones.filter(zona_id=zona_id)

    ubicaciones_con_datos = []
    for ubi in ubicaciones:
        ocupacion = ubi.ocupacion_actual
        porcentaje = ubi.porcentaje_ocupacion
        disponible = ubi.capacidad_maxima - ocupacion
        ubicaciones_con_datos.append({
            'obj': ubi,
            'ocupacion': ocupacion,
            'porcentaje': porcentaje,
            'disponible': disponible,
        })

    if estado:
        if estado == 'vacia':
            ubicaciones_con_datos = [u for u in ubicaciones_con_datos if u['porcentaje'] == 0]
        elif estado == 'baja':
            ubicaciones_con_datos = [u for u in ubicaciones_con_datos if 0 < u['porcentaje'] < 70]
        elif estado == 'alta':
            ubicaciones_con_datos = [u for u in ubicaciones_con_datos if 70 <= u['porcentaje'] < 90]
        elif estado == 'llena':
            ubicaciones_con_datos = [u for u in ubicaciones_con_datos if u['porcentaje'] >= 90]

    paginator = Paginator(ubicaciones_con_datos, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    bodegas = Bodega.objects.filter(activo=True).order_by('codigo')
    zonas = Zona.objects.filter(activo=True).select_related('bodega').order_by('bodega__codigo', 'codigo')

    total_ubicaciones = Ubicacion.objects.filter(activo=True).count()
    capacidad_total = Ubicacion.objects.filter(activo=True).aggregate(
        total=Sum('capacidad_maxima')
    )['total'] or 0

    from apps.inventario.models import Existencia
    ocupacion_total = Existencia.objects.aggregate(total=Sum('cantidad'))['total'] or 0
    porcentaje_global = round((ocupacion_total / capacidad_total) * 100, 1) if capacidad_total > 0 else 0

    ubicaciones_llenas = sum(
        1 for u in Ubicacion.objects.filter(activo=True)
        if u.porcentaje_ocupacion >= 90
    )

    context = {
        'page_obj': page_obj,
        'bodegas': bodegas,
        'zonas': zonas,
        'total_ubicaciones': total_ubicaciones,
        'capacidad_total': capacidad_total,
        'ocupacion_total': ocupacion_total,
        'porcentaje_global': porcentaje_global,
        'ubicaciones_llenas': ubicaciones_llenas,
        'filtros': {
            'q': q,
            'bodega': bodega_id,
            'zona': zona_id,
            'estado': estado,
        }
    }

    return render(request, 'almacen/ubicacion_lista.html', context)


@login_required
def ubicacion_detalle(request, codigo):
    """
    Detalle de una ubicación específica.
    """
    from apps.almacen.models import Ubicacion, MovimientoUbicacion
    from apps.inventario.models import Existencia

    ubicacion = get_object_or_404(Ubicacion, codigo=codigo)

    existencias = Existencia.objects.filter(
        ubicacion=ubicacion,
        cantidad__gt=0
    ).select_related('producto')

    movimientos = MovimientoUbicacion.objects.filter(
        ubicacion=ubicacion
    ).select_related('producto', 'usuario').order_by('-fecha')[:20]

    context = {
        'ubicacion': ubicacion,
        'existencias': existencias,
        'movimientos': movimientos,
    }

    return render(request, 'almacen/ubicacion_detalle.html', context)


@login_required
def mapa_almacen(request, bodega_id=None):
    """
    Mapa visual del almacén.
    """
    from apps.almacen.models import Ubicacion, Zona, Bodega

    bodegas = Bodega.objects.filter(activo=True).order_by('codigo')

    if bodega_id:
        bodega = get_object_or_404(Bodega, id=bodega_id)
    else:
        bodega = bodegas.first()

    zonas = []
    if bodega:
        zonas = Zona.objects.filter(bodega=bodega, activo=True).order_by('codigo')

    context = {
        'bodegas': bodegas,
        'bodega': bodega,
        'zonas': zonas,
    }

    return render(request, 'almacen/mapa_almacen.html', context)