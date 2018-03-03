from django.shortcuts import render, redirect
from .models import Curso
from eventos.models import Evento
from django.views import generic
from .forms import CursosForm


# class CreaCurso(generic.CreateView):
#     model = Curso
#     form_class = CursosForm
#     # fields = ['Nombre', 'Fecha', 'Direccion', 'Descripcion', 'Hora', 'Costo', 'Evento']
#     template_name = 'cursos/nuevo_curso.html'


def nuevo_curso(request):
    NewFormCurso = CursosForm()
    if request.method == 'POST':
        return True;
        # NewActividadForm = FormaActividad(request.POST)
        # if NewActividadForm.is_valid():
        #     actividad = NewActividadForm.save()
        #     return redirect('prospectos:actividades')
        # context = {
        #     'form': NewActividadForm,
        #     'titulo': 'Agregar actividad.',
        #     'error_message': NewActividadForm.errors
        # }
        # return render(request, 'actividades/crear_actividad.html', context)
        # context = {
        #     'form': NewActividadForm,
        #     'titulo': 'Agregar actividad.'
        # }
        # eventos = Evento.objects.all()
    context = {
        'form': NewFormCurso,
        'titulo': 'Agregar curso.',
        'eventos': Evento.objects.all().order_by('Nombre')
    }

    return render(request, 'cursos/nuevo_curso.html', context)
