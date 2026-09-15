# Arquitectura del Sistema WMS TechStock

## Estructura de carpetas

## Ruta URL → Vista → Modelo → Plantilla

| URL | Vista | Modelo | Plantilla |
|-----|-------|--------|-----------|
| `/` | core.views.home | Movimiento | core/home.html |
| `/catalogo/productos/` | catalogo.views.producto_lista | Producto | catalogo/producto_lista.html |
| `/almacen/ubicaciones/` | almacen.views.ubicacion_lista | Ubicacion | almacen/ubicacion_lista.html |
| `/almacen/mapa/` | almacen.views.mapa_almacen | Ubicacion | almacen/mapa_almacen.html |
| `/inventario/kardex/` | inventario.views.kardex | Movimiento | inventario/kardex.html |
| `/recepcion/ordenes/` | recepcion.views.orden_lista | OrdenRecepcion | recepcion/orden_lista.html |
| `/despacho/pedidos/` | despacho.views.pedido_lista | Pedido | despacho/pedido_lista.html |

## Flujo de una petición

## Modelos por aplicación

| App | Modelos |
|-----|---------|
| catalogo | Categoria, Marca, UnidadMedida, Proveedor, Producto |
| almacen | Bodega, Zona, Ubicacion, MovimientoUbicacion |
| inventario | Existencia, Movimiento |
| recepcion | OrdenRecepcion, LineaRecepcion |
| despacho | Cliente, Pedido, LineaPedido |
| usuarios | Usuario |

## Tecnologías

- Backend: Django 5.2 LTS
- Base de datos: SQLite (desarrollo) / PostgreSQL (producción)
- Frontend: Tailwind CSS 3 + Flowbite + Alpine.js
- Admin: Django Unfold
- Import/Export: django-import-export

## Decisiones de diseño

1. Saldo e historial son tablas distintas
2. Existencia única por producto+ubicación
3. Borrado lógico (activo=False)
4. DecimalField para cantidades y dinero
5. Transacciones atómicas en services.py
6. Kardex de solo lectura