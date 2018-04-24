from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required
from prospectos.models import Actividad

# US21
@login_required
@group_required('vendedora', 'administrador')
def index(request):
    agenda = Actividad.objects.filter(terminado=False).order_by('fecha', 'hora')
    bitacora = Actividad.objects.filter(terminado=True).order_by('fecha', 'hora')
    context = {
        'agenda': agenda,
        'bitacora': bitacora,
        'titulo': 'Pendientes',
        }
    return render(request, 'index/index.html', context)


@login_required
@group_required('vendedora', 'admininistrador')
def regresar(request, url):
    return redirect(request.META.get('HTTP_REFERER', '/'))
