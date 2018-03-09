from django.shortcuts import render, redirect
from .models import Evento
from .forms import EventoForm
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required


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
#ID 32
def crear_evento(request):
    #Crea la forma en la vista
    NewEventoForm = EventoForm()
    #Pide el metodo post
    if request.method == 'POST':
        NewEventoForm = EventoForm(request.POST or None)
        #Valida la forma, la guarda y redirecciona
        if NewEventoForm.is_valid():
            Evento = NewEventoForm.save(commit=False)
            Evento.save()
            return redirect('eventos:lista_evento')
        #Envia la informacion necesaria.
        context = {
            'NewEventoForm': NewEventoForm,
            'titulo': 'Registrar un Evento',
        }
        return render(request, 'eventos/crear_evento.html', context)
    context = {
        'NewEventoForm': NewEventoForm,
        'titulo': 'Registrar un Evento',
    }
    return render(request, 'eventos/crear_evento.html', context)
