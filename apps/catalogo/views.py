from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def producto_lista(request):
    return render(request, 'catalogo/producto_lista.html')
