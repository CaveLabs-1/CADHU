from django.shortcuts import render, redirect
from .models import Prospecto, Lugar, Actividad
from django.views import generic
from .forms import FormaActividad, ProspectoForm, LugarForm

def lista_prospecto(request):
    prospectos = Prospecto.objects.all()
    return render(request, 'prospectos/prospectos.html', {'prospectos':prospectos})

# Create your views here.
def prospecto_crear(request):
    NewProspectoForm = ProspectoForm()
    NewLugarForm = LugarForm()
    if request.method == 'POST':
        NewProspectoForm = ProspectoForm(request.POST)
        NewLugarForm = LugarForm(request.POST)
        if NewProspectoForm.is_valid() and NewLugarForm.is_valid():
            Lugar = NewLugarForm.save()
            Prospecto = NewProspectoForm.save(commit=False)
            Prospecto.Direccion = Lugar
            Prospecto.save()
            return prospecto_lista(request)
        context = {
            'NewProspectoForm': NewProspectoForm,
            'NewLugarForm': NewLugarForm,
        }
        return render(request, 'prospectos/prospectos_form.html', context)
    context = {
        'NewProspectoForm': NewProspectoForm,
        'NewLugarForm': NewLugarForm,
    }
    return render(request, 'prospectos/prospectos_form.html', context)


def prospecto_lista(request):
    Prospecto = Prospecto.objects.all()
    context = {
        'Prospecto': Prospecto,
    }
    return render(request, 'prospecto/prospecto_lista.html',context)


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
