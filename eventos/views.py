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
    return render(request, 'eventos/eventos.html', {'eventos':eventos})

@login_required
@group_required('administrador')
def crear_evento(request):
    NewEventoForm = EventoForm(request.POST or None)

    if NewEventoForm.is_valid():
        Evento = NewEventoForm.save(commit=False)
        Evento.save()
        return redirect('eventos:lista_eventos')
    return render(request, 'eventos/crear_evento.html', {'NewEventoForm': NewEventoForm})

    # NewProspectoForm = ProspectoForm()
    # NewLugarForm = LugarForm()
    # if request.method == 'POST':
    #     Error = 'Forma invalida, favor de revisar sus respuestas'
    #     NewProspectoForm = ProspectoForm(request.POST)
    #     NewLugarForm = LugarForm(request.POST)
    #     if NewProspectoForm.is_valid() and NewLugarForm.is_valid():
    #         Lugar = NewLugarForm.save()
    #         Prospecto = NewProspectoForm.save(commit=False)
    #         Prospecto.Direccion = Lugar
    #         Prospecto.save()
    #         return lista_prospectos(request)
    #     context = {
    #         'Error': Error,
    #         'NewProspectoForm': NewProspectoForm,
    #         'NewLugarForm': NewLugarForm,
    #         'titulo': 'Registrar un Prospecto',
    #     }
    #     return render(request, 'prospectos/prospectos_form.html', context)
    # context = {
    #     'NewProspectoForm': NewProspectoForm,
    #     'NewLugarForm': NewLugarForm,
    #     'titulo': 'Registrar un Prospecto',
    # }
    # return render(request, 'prospectos/prospectos_form.html', context)