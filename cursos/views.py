from django.shortcuts import render, redirect
from .models import Curso
from prospectos.models import ProspectoEvento
from eventos.models import Evento
from django.views import generic
from .forms import FormaCurso
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required

# US29
@login_required
@group_required('administrador')
def cursos(request):
    context = {
        'titulo': 'Grupo',
        # 'eventos': Evento.objects.all().order_by('Nombre'),
        'cursos': Curso.objects.filter(Activo = True),
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
        'eventos': Evento.objects.filter(Activo = True).order_by('Nombre')
    }
    return render(request, 'cursos/nuevo_curso.html', context)

#US 28
@login_required
@group_required('vendedora','administrador')
def eliminar_grupo(request, id):
    # evento = Evento.objects.get(id=id)
    curso = Curso.objects.get(id=id)
    gruposUtilizados = ProspectoEvento.objects.filter(Curso_id = curso.id).count()
    # print(id)
    # print(curso)

    if(gruposUtilizados > 0):
        curso.Activo = False
        curso.save()
        # print(evento.Activo)
        return redirect('cursos:cursos')
    else:
        curso.delete()
        return redirect('cursos:cursos')


@login_required
@group_required('vendedora','administrador')
def editar_grupo(request, id):
    #Hacer asignaciones desde la BD
    grupo = Curso.objects.get(id=id)
    forma_curso = FormaCurso(instance=grupo)

    #Checar que el metodo sea POST
    if request.method == 'POST':
        forma_curso = FormaCurso(request.POST or None, instance=grupo)

        #Checar que la forma sea valida y guardarla
        if forma_curso.is_valid():
            forma_curso.save()
            messages.success(request, '¡Grupo editado exitosamente!')
            return redirect('/cursos/lista_cursos')

        #Si la forma no es valida, hacer render y mandar errores
        context = {
            'form': forma_curso,
            'titulo': 'Editar Grupo',
            'error_message': forma_curso.errors
        }
        return redirect('cursos:editar_grupo', id=id)

    #Render a la pagina
    context = {
        'form': forma_curso,
        'titulo': 'Editar Grupo',
        'eventos': Evento.objects.filter(Activo = True).order_by('Nombre')
    }
    return render(request, 'cursos/editar_curso.html', context)