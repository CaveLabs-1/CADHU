from django.shortcuts import render, redirect
from .models import Curso
from eventos.models import Evento
from django.views import generic
from .forms import FormaCurso
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required

# class CreaCurso(generic.CreateView):
#     model = Curso
#     form_class = CursosForm
#     # fields = ['Nombre', 'Fecha', 'Direccion', 'Descripcion', 'Hora', 'Costo', 'Evento']
#     template_name = 'cursos/nuevo_curso.html'

@login_required
@group_required('administrador')
def nuevo_curso(request):
    # NewActividadForm = FormaActividad()
    Forma_nuevo_curso = FormaCurso()
    if request.method == 'POST':
        # NewActividadForm = FormaActividad(request.POST)
        Forma_nuevo_curso = FormaCurso(request.POST)
        if Forma_nuevo_curso.is_valid():
            actividad = Forma_nuevo_curso.save()
            return redirect('/login')
        # else:
        #     print ("Error")
        #     print (Forma_nuevo_curso.errors)
        context = {
            'form': Forma_nuevo_curso,
            'titulo': 'Agregar curso.',
            'error_message': Forma_nuevo_curso.errors
        }
        return render(request, 'cursos/nuevo_curso.html', context)
    context = {
        'form': Forma_nuevo_curso,
        'titulo': 'Agregar curso.',
        'eventos': Evento.objects.all().order_by('Nombre')
    }
    return render(request, 'cursos/nuevo_curso.html', context)

# def nuevo_curso(request):
#     Forma_Curso = CursosForm()
#     if request.method == 'POST':
#         # return True;
#         Nuevo_Curso = Forma_Curso(request.POST)
#         if Nuevo_Curso.is_valid():
#             curso = Nuevo_Curso.save()
#             return redirect('prospectos:actividades')
#         context = {
#             'form': Nuevo_Curso,
#             'titulo': 'Agregar curso.',
#             'error_message': Nuevo_Curso.errors
#         }
#
#     context = {
#         'form': Forma_Curso,
#         'titulo': 'Agregar curso.',
#         'eventos': Evento.objects.all().order_by('Nombre')
#     }
#
#     return render(request, 'cursos/nuevo_curso.html', context)
