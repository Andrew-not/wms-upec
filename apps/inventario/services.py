"""
Servicios de inventario.
Todas las operaciones que modifican el stock pasan por aquí.
Usan transacciones atómicas para garantizar consistencia.
"""
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Existencia, Movimiento
from apps.catalogo.models import Producto
from apps.almacen.models import Ubicacion


class StockInsuficienteError(ValidationError):
    """Error cuando no hay stock suficiente para una salida."""
    pass


class CapacidadExcedidaError(ValidationError):
    """Error cuando la ubicación destino no tiene capacidad."""
    pass


# =====================================================
# FUNCIÓN AUXILIAR: obtener o crear existencia
# =====================================================

def _get_or_create_existencia(producto, ubicacion):
    """Obtiene o crea una existencia (producto + ubicación)."""
    existencia, _ = Existencia.objects.get_or_create(
        producto=producto,
        ubicacion=ubicacion,
        defaults={'cantidad': 0, 'cantidad_reservada': 0}
    )
    return existencia


# =====================================================
# SERVICIO 1: REGISTRAR ENTRADA
# =====================================================

@transaction.atomic
def registrar_entrada(producto, ubicacion, cantidad, usuario,
                      documento='', observacion=''):
    """
    Registra la entrada de mercadería a una ubicación.
    
    Args:
        producto: instancia de Producto
        ubicacion: instancia de Ubicacion destino
        cantidad: int > 0
        usuario: instancia de Usuario
        documento: str opcional (N° de factura, guía, etc.)
        observacion: str opcional
    
    Returns:
        Movimiento creado
    
    Raises:
        ValidationError: si cantidad <= 0 o capacidad excedida
    """
    if cantidad <= 0:
        raise ValidationError('La cantidad debe ser mayor a cero.')
    
    if not producto.activo:
        raise ValidationError(f'El producto {producto.sku} está inactivo.')
    
    if not ubicacion.activo:
        raise ValidationError(f'La ubicación {ubicacion.codigo} está inactiva.')
    
    # Verificar capacidad
    existencia = _get_or_create_existencia(producto, ubicacion)
    if existencia.cantidad + cantidad > ubicacion.capacidad_maxima:
        raise CapacidadExcedidaError(
            f'Capacidad excedida en {ubicacion.codigo}. '
            f'Actual: {existencia.cantidad}, '
            f'Máximo: {ubicacion.capacidad_maxima}, '
            f'Intento: +{cantidad}'
        )
    
    # Actualizar existencia
    existencia.cantidad += cantidad
    existencia.save()
    
    # Crear movimiento
    movimiento = Movimiento.objects.create(
        tipo='ENTRADA',
        producto=producto,
        cantidad=cantidad,
        ubicacion_destino=ubicacion,
        documento=documento,
        observacion=observacion,
        usuario=usuario,
        fecha_movimiento=timezone.now().date(),
    )
    
    return movimiento


# =====================================================
# SERVICIO 2: REGISTRAR SALIDA
# =====================================================

@transaction.atomic
def registrar_salida(producto, ubicacion, cantidad, usuario,
                     documento='', observacion=''):
    """
    Registra la salida de mercadería desde una ubicación.
    VALIDA que haya stock suficiente.
    
    Raises:
        StockInsuficienteError: si no hay suficiente stock
    """
    if cantidad <= 0:
        raise ValidationError('La cantidad debe ser mayor a cero.')
    
    # Verificar que exista la existencia
    try:
        existencia = Existencia.objects.select_for_update().get(
            producto=producto,
            ubicacion=ubicacion
        )
    except Existencia.DoesNotExist:
        raise StockInsuficienteError(
            f'No existe stock de {producto.sku} en {ubicacion.codigo}.'
        )
    
    # Bloqueo select_for_update para evitar condiciones de carrera
    if existencia.cantidad_disponible < cantidad:
        raise StockInsuficienteError(
            f'Stock insuficiente de {producto.sku} en {ubicacion.codigo}. '
            f'Disponible: {existencia.cantidad_disponible}, '
            f'Solicitado: {cantidad}'
        )
    
    # Actualizar existencia
    existencia.cantidad -= cantidad
    existencia.save()
    
    # Crear movimiento
    movimiento = Movimiento.objects.create(
        tipo='SALIDA',
        producto=producto,
        cantidad=cantidad,
        ubicacion_origen=ubicacion,
        documento=documento,
        observacion=observacion,
        usuario=usuario,
        fecha_movimiento=timezone.now().date(),
    )
    
    return movimiento


# =====================================================
# SERVICIO 3: REGISTRAR TRASLADO
# =====================================================

@transaction.atomic
def registrar_traslado(producto, ubicacion_origen, ubicacion_destino,
                       cantidad, usuario, documento='', observacion=''):
    """
    Mueve mercadería de una ubicación a otra.
    Valida stock en origen y capacidad en destino.
    """
    if cantidad <= 0:
        raise ValidationError('La cantidad debe ser mayor a cero.')
    
    if ubicacion_origen == ubicacion_destino:
        raise ValidationError('La ubicación origen y destino no pueden ser la misma.')
    
    # Verificar stock en origen
    try:
        existencia_origen = Existencia.objects.select_for_update().get(
            producto=producto,
            ubicacion=ubicacion_origen
        )
    except Existencia.DoesNotExist:
        raise StockInsuficienteError(
            f'No existe stock de {producto.sku} en {ubicacion_origen.codigo}.'
        )
    
    if existencia_origen.cantidad_disponible < cantidad:
        raise StockInsuficienteError(
            f'Stock insuficiente para traslado. '
            f'Disponible en {ubicacion_origen.codigo}: '
            f'{existencia_origen.cantidad_disponible}, Solicitado: {cantidad}'
        )
    
    # Verificar capacidad en destino
    existencia_destino = _get_or_create_existencia(producto, ubicacion_destino)
    if existencia_destino.cantidad + cantidad > ubicacion_destino.capacidad_maxima:
        raise CapacidadExcedidaError(
            f'Capacidad excedida en destino {ubicacion_destino.codigo}.'
        )
    
    # Actualizar origen
    existencia_origen.cantidad -= cantidad
    existencia_origen.save()
    
    # Actualizar destino
    existencia_destino.cantidad += cantidad
    existencia_destino.save()
    
    # Crear movimiento
    movimiento = Movimiento.objects.create(
        tipo='TRASLADO',
        producto=producto,
        cantidad=cantidad,
        ubicacion_origen=ubicacion_origen,
        ubicacion_destino=ubicacion_destino,
        documento=documento,
        observacion=observacion,
        usuario=usuario,
        fecha_movimiento=timezone.now().date(),
    )
    
    return movimiento


# =====================================================
# SERVICIO 4: REGISTRAR AJUSTE
# =====================================================

@transaction.atomic
def registrar_ajuste(producto, ubicacion, cantidad_nueva, usuario,
                     observacion='', documento=''):
    """
    Ajusta la cantidad de una existencia al valor real (conteo físico).
    Registra la diferencia como AJUSTE_POS o AJUSTE_NEG.
    """
    if cantidad_nueva < 0:
        raise ValidationError('La cantidad no puede ser negativa.')
    
    if not observacion:
        raise ValidationError('El ajuste requiere una observación obligatoria.')
    
    existencia = _get_or_create_existencia(producto, ubicacion)
    diferencia = cantidad_nueva - existencia.cantidad
    
    if diferencia == 0:
        raise ValidationError('No hay diferencia que ajustar.')
    
    # Determinar tipo de ajuste
    tipo = 'AJUSTE_POS' if diferencia > 0 else 'AJUSTE_NEG'
    
    # Actualizar existencia
    existencia.cantidad = cantidad_nueva
    existencia.save()
    
    # Crear movimiento
    movimiento = Movimiento.objects.create(
        tipo=tipo,
        producto=producto,
        cantidad=abs(diferencia),
        ubicacion_origen=ubicacion if diferencia < 0 else None,
        ubicacion_destino=ubicacion if diferencia > 0 else None,
        documento=documento,
        observacion=f'Ajuste de {diferencia:+d}. {observacion}',
        usuario=usuario,
        fecha_movimiento=timezone.now().date(),
    )
    
    return movimiento