# Módulo de Inventario

## ¿Qué hace?

Controla las existencias, el kardex y las operaciones de entrada, salida, traslado y ajuste.

## Modelos

### Existencia
Saldo actual de un producto en una ubicación.

| Campo | Tipo |
|-------|------|
| producto | FK a Producto |
| ubicacion | FK a Ubicacion |
| cantidad | Integer |
| cantidad_reservada | Integer |

Restricción: unique_together = [['producto', 'ubicacion']]

### Movimiento (Kardex)
Registro histórico de solo lectura.

| Campo | Tipo |
|-------|------|
| tipo | ENTRADA, SALIDA, TRASLADO, AJUSTE_POS, AJUSTE_NEG |
| producto | FK |
| cantidad | Integer |
| ubicacion_origen | FK |
| ubicacion_destino | FK |
| documento | CharField |
| usuario | FK |
| fecha | DateTime |

## Servicios

- registrar_entrada(producto, ubicacion, cantidad, usuario)
- registrar_salida(producto, ubicacion, cantidad, usuario) - valida stock
- registrar_traslado(producto, origen, destino, cantidad, usuario)
- registrar_ajuste(producto, ubicacion, cantidad_nueva, usuario)

Todos usan transaction.atomic.

## Cómo probar

### 1. Cargar datos

    python manage.py cargar_datos_demo --reset

### 2. Ver kardex

    http://127.0.0.1:8000/inventario/kardex/

### 3. Probar stock insuficiente

    python manage.py shell

    from apps.inventario.services import registrar_salida, StockInsuficienteError
    from apps.catalogo.models import Producto
    from apps.almacen.models import Ubicacion
    from apps.usuarios.models import Usuario

    prod = Producto.objects.first()
    ubi = Ubicacion.objects.first()
    user = Usuario.objects.first()

    try:
        registrar_salida(prod, ubi, 99999, user)
    except StockInsuficienteError as e:
        print(f"Correcto: {e}")

### 4. Verificar permisos

- Operario: no puede eliminar
- Admin: kardex de solo lectura