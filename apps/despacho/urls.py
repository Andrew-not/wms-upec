from django.urls import path
from . import views

app_name = 'despacho'

urlpatterns = [
    path('pedidos/', views.pedido_lista, name='pedido_lista'),
    path('pedidos/<str:numero>/', views.pedido_detalle, name='pedido_detalle'),
    path('pedidos/<str:numero>/procesar/', views.procesar_picking_view, name='procesar_picking'),
]