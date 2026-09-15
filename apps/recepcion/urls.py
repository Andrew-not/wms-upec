from django.urls import path
from . import views

app_name = 'recepcion'

urlpatterns = [
    path('ordenes/', views.orden_lista, name='orden_lista'),
    path('ordenes/<str:numero>/', views.orden_detalle, name='orden_detalle'),
    path('ordenes/<str:numero>/recibir/', views.recibir_orden, name='recibir_orden'),
]