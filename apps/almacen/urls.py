from django.urls import path
from . import views

app_name = 'almacen'

urlpatterns = [
    path('ubicaciones/', views.ubicacion_lista, name='ubicacion_lista'),
]
