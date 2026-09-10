from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('productos/', views.producto_lista, name='producto_lista'),
]
