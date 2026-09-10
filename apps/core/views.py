from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    """
    Vista de la página principal del WMS.
    Requiere estar autenticado.
    """
    context = {
        'total_productos': 0,
        'total_ubicaciones': 0,
        'total_existencias': 0,
    }
    return render(request, 'core/home.html', context)