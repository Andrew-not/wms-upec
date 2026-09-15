# Módulo de Almacén

## ¿Qué hace?

Gestiona bodegas, zonas, ubicaciones y movimientos de ubicación.

## Modelos

- Bodega
- Zona (RECEPCION, ALMACENAJE, PICKING, DESPACHO, etc.)
- Ubicacion (codigo B1-Z1-E1, tipo, capacidad, peso, volumen)
- MovimientoUbicacion (INGRESO, RETIRO, TRASLADO)

## Funcionalidades

1. Listado con barras de ocupacion
2. Mapa visual del almacen
3. Detalle de ubicacion
4. Filtros por bodega, zona, estado

## Cómo probar

### 1. Listado

    http://127.0.0.1:8000/almacen/ubicaciones/

### 2. Mapa visual

    http://127.0.0.1:8000/almacen/mapa/

### 3. Detalle

    http://127.0.0.1:8000/almacen/ubicaciones/B1-Z1-E1/

### 4. Filtros

- Vacia (0%)
- Baja (menor a 70%)
- Alta (70-90%)
- Llena (mayor o igual a 90%)