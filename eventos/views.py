from django.shortcuts import render, redirect
from .models import Evento
from .forms import EventoForm
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required


@login_required
@group_required('administrador')
def lista_evento(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos/eventos.html', {'eventos':eventos})

@login_required
@group_required('administrador')
def crear_evento(request):
    NewEventoForm = EventoForm()
    if request.method == 'POST':
        NewEventoForm = EventoForm(request.POST or None)
        if NewEventoForm.is_valid():
            Evento = NewEventoForm.save(commit=False)
            Evento.save()
            return redirect('eventos:lista_evento')
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


