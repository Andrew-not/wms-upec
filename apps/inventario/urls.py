from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('kardex/', views.kardex, name='kardex'),
]
