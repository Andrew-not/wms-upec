from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def servicio_inicio(request):
    return render(request, 'servicio/inicio.html')