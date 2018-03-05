from django.shortcuts import render, redirect
from .models import Prospecto, Lugar, Actividad
from datetime import time
from django.views import generic
from .forms import FormaActividad, ProspectoForm, LugarForm
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required

@login_required
@group_required('vendedora','administrador')
def lista_prospectos(request):
    prospectos = Prospecto.objects.all()
    context = {
        'prospectos':prospectos
        }
    return render(request, 'prospectos/prospectos.html', context)

@login_required
@group_required('vendedora','administrador')
def prospecto_crear(request):
    NewProspectoForm = ProspectoForm()
    NewLugarForm = LugarForm()
    if request.method == 'POST':
        Error = 'Forma invalida, favor de revisar sus respuestas'
        NewProspectoForm = ProspectoForm(request.POST)
        NewLugarForm = LugarForm(request.POST)
        if NewProspectoForm.is_valid() and NewLugarForm.is_valid():
            Lugar = NewLugarForm.save()
            Prospecto = NewProspectoForm.save(commit=False)
            Prospecto.Direccion = Lugar
            Prospecto.save()
            return lista_prospectos(request)
        context = {
            'Error': Error,
            'NewProspectoForm': NewProspectoForm,
            'NewLugarForm': NewLugarForm,
            'titulo': 'Registrar un Prospecto',
        }
        return render(request, 'prospectos/prospectos_form.html', context)
    context = {
        'NewProspectoForm': NewProspectoForm,
        'NewLugarForm': NewLugarForm,
        'titulo': 'Registrar un Prospecto',
    }
    return render(request, 'prospectos/prospectos_form.html', context)

@login_required
@group_required('vendedora','administrador')
def editar_prospecto(request, id):
    idprospecto = Prospecto.objects.get(id=id)
    NewProspectoForm = ProspectoForm(request.POST or None, instance=idprospecto)
    NewLugarForm = LugarForm(request.POST or None, instance=idprospecto.Direccion)
    if NewProspectoForm.is_valid() and NewLugarForm.is_valid():

        prospecto = NewProspectoForm.save(commit=False)
        Lugar = NewLugarForm.save()
        Prospecto.Direccion =Lugar
        prospecto.save()
        return lista_prospectos(request)
    context = {
        'NewProspectoForm': NewProspectoForm,
        'NewLugarForm': NewLugarForm,
        'prospecto': idprospecto,
    }
    return render(request, 'prospectos/prospectos_form.html', context)


class ListaActividades(generic.ListView):
    model = Actividad
    template_name = 'actividades/actividades.html'
    context_object_name = 'actividades'

    def get_queryset(self):
        return Actividad.objects.all().order_by('fecha').order_by('hora').order_by('titulo')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListaActividades, self).get_context_data(**kwargs)
        context['titulo'] = 'Actividades'
        context['agrega'] = 'Agregar actividad'
        return context

@login_required
@group_required('vendedora','administrador')
def crearActividad(request):
    NewActividadForm = FormaActividad()
    if request.method == 'POST':
        NewActividadForm = FormaActividad(request.POST)
        if NewActividadForm.is_valid():
            actividad = NewActividadForm.save(commit=False)
            # hora = time.strftime(time(int(actividad.hora)), "%I:%M %p")
            # actividad.hora = hora
            actividad.save()
            return redirect('prospectos:actividades')
        else:
            mensaje = ''
            context = {
                'form': NewActividadForm,
                'titulo': 'Agregar actividad',
            }
            for field, errors in NewActividadForm.errors.items():
                for error in errors:
                    mensaje += error
            context['mensaje_error'] = mensaje
            return render(request, 'actividades/crear_actividad.html', context)
    context = {
        'form': NewActividadForm,
        'titulo': 'Agregar actividad'
    }
    return render(request, 'actividades/crear_actividad.html', context)
