from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required

@login_required
@group_required('vendedora','administrador')
def index(request):
    context = {
        'titulo': 'Pendientes',
        }
    return render(request, 'index/index.html', context)
