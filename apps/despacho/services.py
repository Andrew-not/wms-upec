from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Pedido, LineaPedido
from apps.inventario.services import registrar_salida, StockInsuficienteError


@transaction.atomic
def procesar_picking(pedido, usuario, observacion=''):
    """
    Procesa el picking de un pedido completo.
    Valida stock disponible y descuenta.
    Si no hay stock suficiente, lanza error y no se hace nada.
    """
    if pedido.estado not in ['PENDIENTE', 'PICKING']:
        raise ValidationError(
            f'No se puede hacer picking de un pedido en estado {pedido.get_estado_display()}'
        )

    pedido.estado = 'PICKING'
    pedido.save()

    for linea in pedido.lineas.all():
        cantidad_pendiente = linea.cantidad - linea.cantidad_preparada

        if cantidad_pendiente <= 0:
            continue

        if not linea.ubicacion_origen:
            raise ValidationError(
                f'La línea de {linea.producto.sku} no tiene ubicación de origen'
            )

        # Esto valida stock y descuenta
        registrar_salida(
            producto=linea.producto,
            ubicacion=linea.ubicacion_origen,
            cantidad=cantidad_pendiente,
            usuario=usuario,
            documento=pedido.numero,
            observacion=f'Picking de pedido {pedido.numero}. {observacion}'
        )

        linea.cantidad_preparada = linea.cantidad
        linea.save()

    if all(l.completa for l in pedido.lineas.all()):
        pedido.estado = 'PREPARADO'
        pedido.save()

    return pedido


@transaction.atomic
def despachar_pedido(pedido, usuario, observacion=''):
    """
    Marca el pedido como despachado.
    """
    if pedido.estado != 'PREPARADO':
        raise ValidationError('El pedido debe estar PREPARADO antes de despachar')

    pedido.estado = 'DESPACHADO'
    pedido.fecha_despacho = timezone.now().date()
    pedido.usuario_despacho = usuario
    pedido.save()

    return pedido