from django.shortcuts import render, redirect
from .models import Prospecto, Lugar, Actividad
from django.views import generic
from .forms import FormaActividad, ProspectoForm, LugarForm
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required

def lista_prospecto(request):
    prospectos = Prospecto.objects.all()
    return render(request, 'prospectos/prospectos.html', {'prospectos':prospectos})

@login_required
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
            return lista_prospecto(request)
        context = {
            'Error': Error,
            'NewProspectoForm': NewProspectoForm,
            'NewLugarForm': NewLugarForm,
        }
        return render(request, 'prospectos/prospectos_form.html', context)
    context = {
        'NewProspectoForm': NewProspectoForm,
        'NewLugarForm': NewLugarForm,
    }
    return render(request, 'prospectos/prospectos_form.html', context)

def prospecto_editar(request):
    prospecto = Prospecto.objects.get(id=id)
    form = ProspectoForm(request.POST or None, instance=prospecto)
    formlugar = LugarForm(request.Post or None, instance=Lugar)
    if form.is_valid():
        form.save()
        return redirect('prospectos')

    return render(request, 'prospectos_form.html',{'form':form, 'Lugar':formlugar, 'prospectos':prospecto})


class ListaActividades(generic.ListView):
    model = Actividad
    template_name = 'actividades/actividades.html'
    context_object_name = 'actividades'

    def get_queryset(self):
        return Actividad.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListaActividades, self).get_context_data(**kwargs)
        context['titulo'] = 'Actividades.'
        context['agrega'] = 'Agregar actividad'
        return context


def crearActividad(request):
    NewActividadForm = FormaActividad()
    if request.method == 'POST':
        NewActividadForm = FormaActividad(request.POST)
        if NewActividadForm.is_valid():
            actividad = NewActividadForm.save()
            return redirect('prospectos:actividades')
        context = {
            'form': NewActividadForm,
            'titulo': 'Agregar actividad.',
            'error_message': NewActividadForm.errors
        }
        return render(request, 'actividades/crear_actividad.html', context)
    context = {
        'form': NewActividadForm,
        'titulo': 'Agregar actividad.'
    }
    return render(request, 'actividades/crear_actividad.html', context)
