from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    """
    Vista de la página principal del WMS
    """
    return render(request, 'core/home.html')