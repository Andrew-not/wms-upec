# Módulo de Catálogo

## ¿Qué hace?

Gestiona productos, categorías, marcas, unidades de medida y proveedores.

## Modelos

- Categoria
- Marca
- UnidadMedida
- Proveedor
- Producto (con SKU unico, codigo de barras, imagen, peso, clasificacion ABC)

## Funcionalidades

1. Admin con buscador por SKU, nombre o codigo de barras
2. Filtros por marca, categoria y clasificacion ABC
3. Import/Export Excel
4. Cards 3D en el frontend
5. Paginacion

## Cómo probar

### 1. Ver catalogo

    http://127.0.0.1:8000/catalogo/productos/

### 2. Filtrar

- Buscar "iPhone"
- Filtrar por marca "Apple"

### 3. Import/Export

    http://127.0.0.1:8000/admin/catalogo/producto/

Botones: Importar, Exportar