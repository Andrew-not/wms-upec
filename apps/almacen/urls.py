from django.urls import path
from . import views

app_name = 'almacen'

urlpatterns = [
    path('ubicaciones/', views.ubicacion_lista, name='ubicacion_lista'),
    path('ubicaciones/<str:codigo>/', views.ubicacion_detalle, name='ubicacion_detalle'),
    path('mapa/', views.mapa_almacen, name='mapa_almacen'),
    path('mapa/<int:bodega_id>/', views.mapa_almacen, name='mapa_almacen_bodega'),
]