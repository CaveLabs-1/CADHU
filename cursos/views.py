from django.shortcuts import render, redirect, reverse
from .models import Curso
from grupos.models import Grupo
from .forms import CursoForm
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required
from django.contrib import messages

# US36 y US34
@login_required
@group_required('vendedora', 'administrador')
def lista_cursos(request):
    # Se hacer render de la lista de prospectos
    cursos = Curso.objects.filter(activo=True)
    context = {
        'cursos': cursos,
        'titulo': 'Cursos',
    }
    return render(request, 'cursos/cursos.html', context)

# US32
@login_required
@group_required('administrador')
def crear_curso(request):
    # Crea la forma en la vista
    new_curso_form = CursoForm()
    # Pide el método post
    if request.method == 'POST':
        new_curso_form = CursoForm(request.POST or None)
        # Valida la forma, la guarda y redirecciona
        if new_curso_form.is_valid():
            curso = new_curso_form.save(commit=False)
            curso.activo = True
            curso.save()
            # Mensaje de exito
            messages.success(request, 'El curso ha sido creado.')
            return redirect(reverse('cursos:lista_cursos'))
        else:
            # Mensaje de error
            messages.success(request, 'Existe una falla en los campos.')
            # Envia la información necesaria.
            context = {
                'new_curso_form': new_curso_form,
                'titulo': 'Registrar un Grupo',
            }
            return render(request, 'cursos/form_curso.html', context)
    context = {
        'new_curso_form': new_curso_form,
        'titulo': 'Registrar un Grupo',
    }
    return render(request, 'cursos/form_curso.html', context)

#US 35
@login_required
@group_required('vendedora', 'administrador')
def eliminar_curso(request, pk):
    curso = Curso.objects.get(id=pk)
    grupos = Grupo.objects.filter(curso_id=pk).count()
    if grupos > 0:
        curso.activo = False
        curso.save()
        return redirect('cursos:lista_cursos')
    else:
        curso.delete()
        return redirect('cursos:lista_cursos')


# US 33
@login_required
@group_required('vendedora', 'administrador')
def editar_curso(request, pk):
    # Obtener el pk del evento, hacer nueva forma del evento
    id_curso = Curso.objects.get(id=pk)
    new_curso_form = CursoForm(instance=id_curso)
    if request.method == 'POST':
        new_curso_form = CursoForm(request.POST or None, instance=id_curso)
        # Si es válida, instanciar nueva empresa Y guardarla
        if new_curso_form.is_valid():
            curso = new_curso_form.save(commit=False)
            curso.activo = True
            curso.save()
            messages.success(request, 'El curso ha sido actualizado.')
            return redirect('cursos:lista_cursos')
        else:
            # Si no es válida, notificar al usuario
            messages.success(request, 'Existe una falla en los campos.')
            context = {
                'new_curso_form': new_curso_form,
                'curso': id_curso,
                'titulo': 'Editar Grupo',
            }
            return render(request, 'cursos/form_curso.html', context)
    context = {
        'new_curso_form': new_curso_form,
        'curso': id_curso,
        'titulo': 'Editar Grupo',
    }
    return render(request, 'cursos/form_curso.html', context)
