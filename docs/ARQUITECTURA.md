# Arquitectura del Sistema C.TECH WMS

## Estructura de carpetas

## Ruta URL → Vista → Modelo → Plantilla

| URL | Vista | Modelo | Plantilla |
|-----|-------|--------|-----------|
| `/` | `core.views.home` | Movimiento, Existencia | `core/home.html` |
| `/mi-espacio/` | `workspace.views.mi_espacio` | TareaPersonal, Evento | `workspace/mi_espacio.html` |
| `/catalogo/productos/` | `catalogo.views.producto_lista` | Producto | `catalogo/producto_lista.html` |
| `/almacen/ubicaciones/` | `almacen.views.ubicacion_lista` | Ubicacion | `almacen/ubicacion_lista.html` |
| `/almacen/mapa/` | `almacen.views.mapa_almacen` | Ubicacion | `almacen/mapa_almacen.html` |
| `/inventario/kardex/` | `inventario.views.kardex` | Movimiento | `inventario/kardex.html` |
| `/recepcion/ordenes/` | `recepcion.views.orden_lista` | OrdenRecepcion | `recepcion/orden_lista.html` |
| `/despacho/pedidos/` | `despacho.views.pedido_lista` | Pedido | `despacho/pedido_lista.html` |
| `/servicio/` | `servicio.views.servicio_inicio` | - | `servicio/inicio.html` |
| `/reportes/` | `reportes.views.reportes_inicio` | - | `reportes/inicio.html` |

## Flujo de una petición

## Modelos por aplicación

| App | Modelos |
|-----|---------|
| `catalogo` | Categoria, Marca, UnidadMedida, Proveedor, Producto |
| `almacen` | Bodega, Zona, Ubicacion |
| `inventario` | Existencia, Movimiento |
| `recepcion` | OrdenRecepcion, LineaRecepcion |
| `despacho` | Cliente, Pedido, LineaPedido |
| `servicio` | EquipoSerie, OrdenServicio, RepuestoUsado (futuro) |
| `workspace` | TareaPersonal, EventoCalendario, NotaRapida, Notificacion, Meta, PreferenciaUsuario, ActividadReciente |
| `usuarios` | Usuario |

## Sistema de roles y jerarquía

| Rol | Acceso `/admin/` | Módulos visibles |
|-----|------------------|-------------------|
| **ADMIN** | ✅ Sí | Todos |
| **JEFE** | ❌ No | Todos excepto admin |
| **OPERARIO** | ❌ No | Su módulo específico |
| **CONSULTA** | ❌ No | Catálogo (solo lectura) |

## Tecnologías

| Capa | Tecnología |
|------|-----------|
| Backend | Django 5.2 LTS |
| Base de datos | SQLite (desarrollo) |
| Frontend | Tailwind CSS 3 + Flowbite + Alpine.js |
| Gráficos | Chart.js |
| Admin | Django Unfold |
| Export PDF | ReportLab |
| Export Excel | openpyxl |
| Export Word | python-docx |

## Decisiones de diseño

1. **Saldo e historial son tablas distintas.** `Existencia` responde "¿cuánto hay ahora?" y se actualiza. `Movimiento` responde "¿qué pasó?" y nunca se modifica.

2. **Unicidad del saldo.** La combinación producto + ubicación es única en `Existencia`.

3. **Borrado lógico.** Los maestros se marcan como `activo = False` en lugar de eliminarse.

4. **DecimalField.** Nunca `FloatField` para cantidades o dinero.

5. **Servicios con transacciones atómicas.** Todas las operaciones pasan por `services.py`.

6. **Kardex de solo lectura.** El admin bloquea agregar, editar y eliminar en `Movimiento`.

7. **Un solo frontend adaptado por rol.** No hay versiones separadas.