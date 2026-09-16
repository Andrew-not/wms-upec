# INFORME TÉCNICO — SISTEMA WMS TECNSTOCK

**Universidad Politécnica Estatal del Carchi**  
**Carrera de Logística y Transporte**  
**Septiembre 2026**

---

## 1. RESUMEN EJECUTIVO

Se desarrolló un Sistema de Gestión de Almacenes (WMS) llamado **TechStock** como aplicación web con Django 5.2 LTS. El sistema permite gestionar el catálogo de productos tecnológicos, la estructura física del almacén, las existencias, los movimientos (kardex), las órdenes de recepción y los pedidos de clientes.

### Tecnologías utilizadas

| Capa | Tecnología |
|------|-----------|
| Backend | Django 5.2 LTS |
| Base de datos | SQLite (desarrollo) |
| Frontend | Tailwind CSS 3 + Flowbite + Alpine.js |
| Admin | Django Unfold |
| Gráficos | Chart.js |

### Módulos implementados

1. **Catálogo** — productos, categorías, marcas, proveedores
2. **Almacén** — bodegas, zonas, ubicaciones, mapa visual
3. **Inventario** — existencias, kardex, servicios transaccionales
4. **Recepción** — órdenes de recepción con putaway
5. **Despacho** — clientes, pedidos, picking con validación de stock

---

## 2. ESQUEMA DE ARQUITECTURA

### Estructura de carpetas

### Ruta URL → Vista → Modelo → Plantilla

| URL | Vista | Modelo | Plantilla |
|-----|-------|--------|-----------|
| `/` | core.views.home | Movimiento | core/home.html |
| `/catalogo/productos/` | catalogo.views.producto_lista | Producto | catalogo/producto_lista.html |
| `/almacen/ubicaciones/` | almacen.views.ubicacion_lista | Ubicacion | almacen/ubicacion_lista.html |
| `/inventario/kardex/` | inventario.views.kardex | Movimiento | inventario/kardex.html |
| `/recepcion/ordenes/` | recepcion.views.orden_lista | OrdenRecepcion | recepcion/orden_lista.html |
| `/despacho/pedidos/` | despacho.views.pedido_lista | Pedido | despacho/pedido_lista.html |

### Flujo de una petición

### Modelo de datos

Principales relaciones:

- Producto ↔ Marca, Categoría, UnidadMedida, Proveedor
- Ubicación ↔ Zona ↔ Bodega
- Existencia ↔ Producto + Ubicación (único)
- Movimiento ↔ Producto + Ubicación origen/destino + Usuario
- OrdenRecepcion ↔ Proveedor → LineaRecepcion ↔ Producto
- Pedido ↔ Cliente → LineaPedido ↔ Producto

---

## 3. CAPTURAS DEL SISTEMA

### 3.1 Dashboard principal

[PEGAR AQUÍ: 01-dashboard.png]

*Figura 1: Dashboard con KPIs en tiempo real (productos, ubicaciones, stock, bajo stock, movimientos del día) y últimos movimientos del kardex.*

### 3.2 Catálogo de productos

[PEGAR AQUÍ: 02-catalogo.png]

*Figura 2: Catálogo con cards visuales, filtros por marca y categoría, badges de stock (En stock, Bajo stock, Agotado).*

### 3.3 Kardex de movimientos

[PEGAR AQUÍ: 03-kardex.png]

*Figura 3: Kardex con filtros por producto, tipo de movimiento y rango de fechas. Solo lectura.*

### 3.4 Almacén

[PEGAR AQUÍ: 04-almacen.png]

*Figura 4: Almacén con barras de ocupación por ubicación, filtros por bodega y zona.*

### 3.5 Prueba de stock insuficiente

[PEGAR AQUÍ: 05-stock-insuficiente.png]

*Figura 5: El sistema rechaza correctamente una salida de 99999 unidades cuando no hay stock suficiente.*

---

## 4. VALIDACIÓN POR PERFILES

### 4.1 Administrador

[PEGAR AQUÍ: 06-admin-superusuario.png]

*Figura 6: El administrador (superusuario) ve todos los módulos en el panel de Django.*

### 4.2 Usuario operario

[PEGAR AQUÍ: 07-admin-operario.png]

*Figura 7: El usuario `operario_catalogo` solo ve su módulo asignado (Catálogo). No puede acceder a otros.*

### 4.3 Pantalla de "Sin acceso"

[PEGAR AQUÍ: 08-sin-acceso.png]

*Figura 8: Cuando el operario intenta acceder a un módulo ajeno, se muestra una pantalla de error 403 personalizada con opción de volver a su módulo.*

### 4.4 Sesión sin autenticación

[PEGAR AQUÍ: 09-operario-frontend.png]

*Figura 9: El operario puede ver el frontend completo pero sin permisos de administración.*

---

## 5. APORTE INDIVIDUAL

| Integrante | Usuario GitHub | Rol | Aporte |
|-----------|----------------|-----|--------|
| Andrés Chalacán | `Andrew-not` | Coordinación + Inventario | Base del proyecto, módulo Inventario, servicios transaccionales, documentación, integración final |
| Roberth Buitrón | `alexis18` | Catálogo | Extensión del catálogo con código de barras, import/export Excel y ficha de producto |
| Wilmer Guanga | `wilmerguanga2005-byte` | Almacén | Extensión del almacén con tipos de ubicación, peso, volumen y mapa visual |
| Damián Tulcán | `leandrinho_14` | Despacho | Módulo de clientes, pedidos y picking con validación de stock |
| John | `trabajouni029-coder` | Recepción | Módulo de órdenes de recepción con putaway automático |

### Enlaces al repositorio

- **Repositorio:** https://github.com/Andrew-not/wms-upec
- **Rama principal:** `main`
- **Rama de desarrollo:** `feature/inventario-base`
- **Pull Request final:** [Enlace al PR]

---

## 6. CONCLUSIONES

1. Se implementó un sistema WMS completo y funcional con 5 módulos integrados.
2. Todas las operaciones de inventario pasan por transacciones atómicas en `services.py`, garantizando la consistencia de los datos.
3. El sistema valida correctamente las operaciones inválidas (stock insuficiente, capacidad excedida) sin dejar registros inconsistentes.
4. Se implementaron 5 perfiles de usuario con permisos diferenciados por módulo, cumpliendo con el principio de mínimo privilegio.
5. El diseño del frontend utiliza Tailwind CSS con tema oscuro profesional, totalmente responsive.

---

**Documento elaborado como material de evaluación para la asignatura de Sistemas de Información Logística.**  
**Universidad Politécnica Estatal del Carchi — 2026**


### Modelo de datos

Principales relaciones:

- Producto ↔ Marca, Categoría, UnidadMedida, Proveedor
- Ubicación ↔ Zona ↔ Bodega
- Existencia ↔ Producto + Ubicación (único)
- Movimiento ↔ Producto + Ubicación origen/destino + Usuario
- OrdenRecepcion ↔ Proveedor → LineaRecepcion ↔ Producto
- Pedido ↔ Cliente → LineaPedido ↔ Producto

---

## 3. CAPTURAS DEL SISTEMA

### 3.1 Dashboard principal

[PEGAR AQUÍ: 01-dashboard.png]

*Figura 1: Dashboard con KPIs en tiempo real (productos, ubicaciones, stock, bajo stock, movimientos del día) y últimos movimientos del kardex.*

### 3.2 Catálogo de productos

[PEGAR AQUÍ: 02-catalogo.png]

*Figura 2: Catálogo con cards visuales, filtros por marca y categoría, badges de stock (En stock, Bajo stock, Agotado).*

### 3.3 Kardex de movimientos

[PEGAR AQUÍ: 03-kardex.png]

*Figura 3: Kardex con filtros por producto, tipo de movimiento y rango de fechas. Solo lectura.*

### 3.4 Almacén

[PEGAR AQUÍ: 04-almacen.png]

*Figura 4: Almacén con barras de ocupación por ubicación, filtros por bodega y zona.*

### 3.5 Prueba de stock insuficiente

[PEGAR AQUÍ: 05-stock-insuficiente.png]

*Figura 5: El sistema rechaza correctamente una salida de 99999 unidades cuando no hay stock suficiente.*

---

## 4. VALIDACIÓN POR PERFILES

### 4.1 Administrador

[PEGAR AQUÍ: 06-admin-superusuario.png]

*Figura 6: El administrador (superusuario) ve todos los módulos en el panel de Django.*

### 4.2 Usuario operario

[PEGAR AQUÍ: 07-admin-operario.png]

*Figura 7: El usuario `operario_catalogo` solo ve su módulo asignado (Catálogo). No puede acceder a otros.*

### 4.3 Pantalla de "Sin acceso"

[PEGAR AQUÍ: 08-sin-acceso.png]

*Figura 8: Cuando el operario intenta acceder a un módulo ajeno, se muestra una pantalla de error 403 personalizada con opción de volver a su módulo.*

### 4.4 Sesión sin autenticación

[PEGAR AQUÍ: 09-operario-frontend.png]

*Figura 9: El operario puede ver el frontend completo pero sin permisos de administración.*

---

## 5. APORTE INDIVIDUAL

| Integrante | Usuario GitHub | Rol | Aporte |
|-----------|----------------|-----|--------|
| Andrés Chalacán | `Andrew-not` | Coordinación + Inventario | Base del proyecto, módulo Inventario, servicios transaccionales, documentación, integración final |
| Roberth Buitrón | `alexis18` | Catálogo | Extensión del catálogo con código de barras, import/export Excel y ficha de producto |
| Wilmer Guanga | `wilmerguanga2005-byte` | Almacén | Extensión del almacén con tipos de ubicación, peso, volumen y mapa visual |
| Damián Tulcán | `leandrinho_14` | Despacho | Módulo de clientes, pedidos y picking con validación de stock |
| John | `trabajouni029-coder` | Recepción | Módulo de órdenes de recepción con putaway automático |

### Enlaces al repositorio

- **Repositorio:** https://github.com/Andrew-not/wms-upec
- **Rama principal:** `main`
- **Rama de desarrollo:** `feature/inventario-base`
- **Pull Request final:** [Enlace al PR]

---

## 6. CONCLUSIONES

1. Se implementó un sistema WMS completo y funcional con 5 módulos integrados.
2. Todas las operaciones de inventario pasan por transacciones atómicas en `services.py`, garantizando la consistencia de los datos.
3. El sistema valida correctamente las operaciones inválidas (stock insuficiente, capacidad excedida) sin dejar registros inconsistentes.
4. Se implementaron 5 perfiles de usuario con permisos diferenciados por módulo, cumpliendo con el principio de mínimo privilegio.
5. El diseño del frontend utiliza Tailwind CSS con tema oscuro profesional, totalmente responsive.

---

**Documento elaborado como material de evaluación para la asignatura de Sistemas de Información Logística.**  
**Universidad Politécnica Estatal del Carchi — 2026**