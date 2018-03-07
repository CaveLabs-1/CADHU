from django.shortcuts import render, redirect
from .models import Evento
from .forms import EventoForm
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required
# Create your views here.

# from eventos.models import Evento
# from django.views import generic
#
#
# class CreaCurso(generic.CreateView):
#     model = Curso
#     fields = ['Nombre', 'Fecha', 'Direccion', 'Descripcion', 'Hora', 'Costo', 'Evento']
#     template_name = 'cursos/nuevo_curso.html'

@login_required
@group_required('administrador')
def lista_evento(request):
    eventos = Evento.objects.all()
    context = {
    'eventos':eventos,
    'titulo': 'Eventos',
    }
    return render(request, 'eventos/eventos.html', context)

@login_required
@group_required('administrador')
def crear_evento(request):
    NewEventoForm = EventoForm(request.POST or None)

    if NewEventoForm.is_valid():
        Evento = NewEventoForm.save(commit=False)
        Evento.save()
        return redirect('eventos:lista_evento')
    return render(request, 'eventos/crear_evento.html', {'NewEventoForm': NewEventoForm})
