# Módulo de Despacho

## ¿Qué hace?

Gestiona clientes, pedidos y picking con validación de stock.

## Modelos

- Cliente (tipo_documento, numero_documento, razon_social)
- Pedido (numero, cliente, prioridad, estado)
- LineaPedido (pedido, producto, cantidad, precio_unitario, ubicacion_origen)

## Servicios

- procesar_picking(pedido, usuario) - descuenta stock, valida disponibilidad
- despachar_pedido(pedido, usuario)

## Cómo probar

### 1. Crear cliente

    http://127.0.0.1:8000/admin/despacho/cliente/add/

### 2. Crear pedido

    http://127.0.0.1:8000/admin/despacho/pedido/add/

Con 3 lineas y ubicacion origen.

### 3. Ver listado

    http://127.0.0.1:8000/despacho/pedidos/

### 4. Procesar picking

1. Clic en "Ver"
2. Clic en "Procesar picking"
3. Stock se descuenta

### 5. Probar stock insuficiente

Pedido con cantidad 9999 - error y rollback