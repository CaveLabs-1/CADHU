from django.shortcuts import render, redirect
from .models import Evento
from .forms import EventoForm
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required
from django.contrib import messages

#US29
@login_required
@group_required('administrador')
def lista_evento(request):
    #Se hacer render de la lista de prospectos
    eventos = Evento.objects.all()
    context = {
    'eventos':eventos,
    'titulo': 'Cursos',
    }
    return render(request, 'eventos/eventos.html', context)

#ID 32
@login_required
@group_required('administrador')
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
            #Mensaje de exito
            messages.success(request, 'El evento ha sido creado.')
            return redirect('eventos:lista_evento')

        else:
            #Mensaje de error
            messages.success(request, 'Existe una falla en los campos.')
        #Envia la informacion necesaria.
            context = {
                'NewEventoForm': NewEventoForm,
                'titulo': 'Registrar un Curso',
            }
            return render(request, 'eventos/crear_evento.html', context)
    context = {
        'NewEventoForm': NewEventoForm,
        'titulo': 'Registrar un Curso',
    }
    return render(request, 'eventos/crear_evento.html', context)

#US 33
@login_required
@group_required('vendedora','administrador')
def editar_evento(request, id):
    #Obtener el id del evento, hacer nueva forma del evento
    idevento = Evento.objects.get(id=id)
    NewEventoForm = EventoForm(instance=idevento)
    if request.method == 'POST':
        NewEventoForm = EventoForm(request.POST or None, instance=idevento)
        #Si es válida, instanciar nueva empresa Y guardarla
        if NewEventoForm.is_valid():
            evento = NewEventoForm.save(commit=False)
            evento.save()
            messages.success(request, 'El curso ha sido actualizado.')
            return redirect('eventos:lista_evento')
        else:
            #Si no es válida, notificar al usuario
            messages.success(request, 'Existe una falla en los campos.')
            context = {
                'NewEventoForm': NewEventoForm,
                'evento': idevento,
                'titulo': 'Editar Curso',
            }
            return render(request, 'eventos/crear_evento.html', context)
    context = {
        'NewEventoForm': NewEventoForm,
        'evento': idevento,
        'titulo': 'Editar Curso',
    }
    return render(request, 'eventos/crear_evento.html', context)
