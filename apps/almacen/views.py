from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def ubicacion_lista(request):
    return render(request, 'almacen/ubicacion_lista.html')
