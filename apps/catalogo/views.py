from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum


@login_required
def producto_lista(request):
    """
    Listado de productos con filtros, búsqueda y paginación.
    Cards con efecto 3D al hacer hover.
    """
    from apps.catalogo.models import Producto, Marca, Categoria

    # Queryset base
    productos = Producto.objects.filter(activo=True).select_related(
        'marca', 'categoria'
    ).order_by('marca__nombre', 'nombre')

    # Filtros
    q = request.GET.get('q', '').strip()
    marca_id = request.GET.get('marca', '')
    categoria_id = request.GET.get('categoria', '')

    if q:
        productos = productos.filter(
            Q(sku__icontains=q) |
            Q(nombre__icontains=q) |
            Q(especificaciones__icontains=q)
        )

    if marca_id:
        productos = productos.filter(marca_id=marca_id)

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    # Paginación
    paginator = Paginator(productos, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Opciones para filtros
    marcas = Marca.objects.filter(activo=True).order_by('nombre')
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')

    # KPIs del catálogo
    total_productos = Producto.objects.filter(activo=True).count()
    stock_total = sum(p.stock_actual for p in Producto.objects.filter(activo=True))
    bajo_stock = sum(1 for p in Producto.objects.filter(activo=True) if p.bajo_stock)

    context = {
        'page_obj': page_obj,
        'marcas': marcas,
        'categorias': categorias,
        'total_productos': total_productos,
        'stock_total': stock_total,
        'bajo_stock': bajo_stock,
        'filtros': {
            'q': q,
            'marca': marca_id,
            'categoria': categoria_id,
        }
    }

    return render(request, 'catalogo/producto_lista.html', context)