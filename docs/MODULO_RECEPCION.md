# Módulo de Recepción

## ¿Qué hace?

Gestiona órdenes de recepción de proveedores y genera movimientos de entrada automáticos.

## Modelos

- OrdenRecepcion (numero, proveedor, estado, fechas)
- LineaRecepcion (orden, producto, cantidad_esperada, cantidad_recibida, ubicacion_destino)

## Servicios

- recibir_linea(linea, cantidad, usuario) - registra entrada en kardex
- recibir_orden_completa(orden, usuario)

## Cómo probar

### 1. Crear orden

    http://127.0.0.1:8000/admin/recepcion/ordenrecepcion/add/

Llena: numero OC-2026-001, proveedor, 3 lineas.

### 2. Ver listado

    http://127.0.0.1:8000/recepcion/ordenes/

### 3. Recibir

1. Clic en "Ver" de una orden
2. Clic en "Recibir orden completa"
3. Estado cambia a RECIBIDA
4. Movimiento aparece en el kardex