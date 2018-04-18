from django.shortcuts import render, redirect
from .models import Curso
from cursos.models import Curso as Grupo
from .forms import CursoForm
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required
from django.contrib import messages

# US36 y US34
@login_required
@group_required('vendedora', 'administrador')
def lista_cursos(request):
    #Se hacer render de la lista de prospectos
    cursos = Curso.objects.filter(Activo = True)
    context = {
    'cursos': cursos,
    'titulo': 'Cursos',
    }
    return render(request, 'eventos/cursos.html', context)

# US32
@login_required
@group_required('administrador')
def crear_curso(request):
    #Crea la forma en la vista
    new_curso_form = CursoForm()
    #Pide el metodo post
    if request.method == 'POST':
        new_curso_form = CursoForm(request.POST or None)
        #Valida la forma, la guarda y redirecciona
        if new_curso_form.is_valid():
            curso = new_curso_form.save(commit=False)
            curso.Activo = True
            curso.save()
            #Mensaje de exito
            messages.success(request, 'El curso ha sido creado.')
            return redirect('eventos:lista_cursos')

        else:
            #Mensaje de error
            messages.success(request, 'Existe una falla en los campos.')
        #Envia la informacion necesaria.
            context = {
                'new_curso_form': new_curso_form,
                'titulo': 'Registrar un Curso',
            }
            return render(request, 'eventos/crear_curso.html', context)
    context = {
        'new_curso_form': new_curso_form,
        'titulo': 'Registrar un Curso',
    }
    return render(request, 'eventos/crear_curso.html', context)

#US 35
@login_required
@group_required('vendedora','administrador')
def eliminar_curso(request, id):
    curso = Curso.objects.get(id=id)
    grupos = Grupo.objects.filter(Evento_id=id).count()
    if(grupos > 0):
        curso.Activo = False
        curso.save()
        return redirect('eventos:lista_cursos')
    else:
        curso.delete()
        return redirect('eventos:lista_cursos')

#US 33
@login_required
@group_required('vendedora','administrador')
def editar_curso(request, id):
    #Obtener el id del evento, hacer nueva forma del evento
    id_curso = Curso.objects.get(id=id)
    new_curso_form = CursoForm(instance=id_curso)
    if request.method == 'POST':
        new_curso_form = CursoForm(request.POST or None, instance=id_curso)
        #Si es válida, instanciar nueva empresa Y guardarla
        if new_curso_form.is_valid():
            curso = new_curso_form.save(commit=False)
            curso.Activo = True
            curso.save()
            messages.success(request, 'El curso ha sido actualizado.')
            return redirect('eventos:lista_evento')
        else:
            #Si no es válida, notificar al usuario
            messages.success(request, 'Existe una falla en los campos.')
            context = {
                'new_curso_form': new_curso_form,
                'curso': id_curso,
                'titulo': 'Editar Curso',
            }
            return render(request, 'eventos/crear_curso.html', context)
    context = {
        'new_curso_form': new_curso_form,
        'curso': id_curso,
        'titulo': 'Editar Curso',
    }
    return render(request, 'eventos/crear_curso.html', context)
