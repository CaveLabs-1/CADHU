from django.shortcuts import render, redirect
from .models import Evento
from .forms import EventoForm
# Create your views here.

def lista_evento(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos/eventos.html', {'eventos':eventos})

def crear_evento(request):
    form = EventoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('eventos:lista_eventos')
    return render(request, 'eventos/crear_evento.html', {'form': form})


