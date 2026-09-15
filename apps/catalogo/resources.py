from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import Producto, Marca, Categoria


class ProductoResource(resources.ModelResource):
    marca = fields.Field(
        column_name='marca',
        attribute='marca',
        widget=ForeignKeyWidget(Marca, 'nombre')
    )
    categoria = fields.Field(
        column_name='categoria',
        attribute='categoria',
        widget=ForeignKeyWidget(Categoria, 'nombre')
    )

    class Meta:
        model = Producto
        fields = (
            'id', 'sku', 'codigo_barras', 'nombre',
            'marca', 'categoria', 'precio_venta',
            'stock_minimo', 'stock_maximo', 'peso_kg',
            'clasificacion_abc', 'activo'
        )
        export_order = fields
        import_id_fields = ('sku',)