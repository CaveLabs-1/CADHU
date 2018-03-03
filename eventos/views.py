from django.shortcuts import render, redirect
from .models import Evento
from .forms import EventoForm
# Create your views here.

# from eventos.models import Evento
# from django.views import generic
#
#
# class CreaCurso(generic.CreateView):
#     model = Curso
#     fields = ['Nombre', 'Fecha', 'Direccion', 'Descripcion', 'Hora', 'Costo', 'Evento']
#     template_name = 'cursos/nuevo_curso.html'

def lista_evento(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos/eventos.html', {'eventos':eventos})

def crear_evento(request):
    form = EventoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('eventos:lista_eventos')
    return render(request, 'eventos/crear_evento.html', {'form': form})
