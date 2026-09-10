from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def kardex(request):
    return render(request, 'inventario/kardex.html')
