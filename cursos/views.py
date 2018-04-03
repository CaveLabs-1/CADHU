from django.shortcuts import render, redirect
from .models import Curso
from eventos.models import Evento
from django.views import generic
from .forms import FormaCurso
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required


@login_required
@group_required('administrador')
def cursos(request):
    context = {
        'titulo': 'Grupo',
        # 'eventos': Evento.objects.all().order_by('Nombre'),
        'cursos': Curso.objects.all(),
    }
    return render(request, 'cursos/cursos.html', context)


@login_required
@group_required('administrador')
def nuevo_curso(request):
    # recibir forma
    Forma_nuevo_curso = FormaCurso()
    # si se recibe una forma con post
    if request.method == 'POST':
        Forma_nuevo_curso = FormaCurso(request.POST)
        # si la forma es válida
        if Forma_nuevo_curso.is_valid():
            # se guarda la forma
            actividad = Forma_nuevo_curso.save()
            # se redirige a la próxima vista
            messages.success(request, '¡Grupo agregado exitosamente!')

            # return redirect('cursos:lista_cursos')
            return redirect('/cursos/lista_cursos')
        # se renderea la forma nuevamente con los errores marcados
        context = {
            'form': Forma_nuevo_curso,
            'titulo': 'Agregar Grupo',
            'error_message': Forma_nuevo_curso.errors
        }
        return render(request, 'cursos/nuevo_curso.html', context)
    # se renderea la página
    context = {
        'form': Forma_nuevo_curso,
        'titulo': 'Agregar Grupo',
        'eventos': Evento.objects.all().order_by('Nombre')
    }
    return render(request, 'cursos/nuevo_curso.html', context)
