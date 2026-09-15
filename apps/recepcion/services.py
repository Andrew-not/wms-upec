from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import OrdenRecepcion, LineaRecepcion
from apps.inventario.services import registrar_entrada


@transaction.atomic
def recibir_linea(linea, cantidad, usuario, observacion=''):
    """
    Registra la recepción de una línea de orden.
    Esto crea un movimiento de ENTRADA en el kardex.
    """
    if cantidad <= 0:
        raise ValidationError('La cantidad debe ser mayor a cero.')

    if linea.cantidad_recibida + cantidad > linea.cantidad_esperada:
        raise ValidationError(
            f'La cantidad excede lo esperado. '
            f'Esperado: {linea.cantidad_esperada}, '
            f'Ya recibido: {linea.cantidad_recibida}, '
            f'Intento: +{cantidad}'
        )

    # Registrar entrada en el inventario
    registrar_entrada(
        producto=linea.producto,
        ubicacion=linea.ubicacion_destino,
        cantidad=cantidad,
        usuario=usuario,
        documento=linea.orden.numero,
        observacion=f'Recepción de orden {linea.orden.numero}. {observacion}'
    )

    # Actualizar la línea
    linea.cantidad_recibida += cantidad
    linea.fecha_recepcion = timezone.now()
    linea.save()

    # Actualizar estado de la orden
    orden = linea.orden
    if all(l.completa for l in orden.lineas.all()):
        orden.estado = 'RECIBIDA'
        orden.fecha_recepcion = timezone.now().date()
        orden.usuario_recepcion = usuario
        orden.save()
    else:
        orden.estado = 'EN_PROCESO'
        orden.save()

    return linea


@transaction.atomic
def recibir_orden_completa(orden, usuario, observacion=''):
    """
    Recibe todas las líneas pendientes de una orden.
    """
    for linea in orden.lineas.all():
        cantidad_pendiente = linea.cantidad_esperada - linea.cantidad_recibida
        if cantidad_pendiente > 0:
            recibir_linea(linea, cantidad_pendiente, usuario, observacion)

    return orden