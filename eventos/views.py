from django.shortcuts import render, redirect
from .models import Curso
from .forms import CursoForm
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required
from django.contrib import messages

# US36 y US34
@login_required
@group_required('vendedora', 'administrador')
def lista_cursos(request):
    #Se hacer render de la lista de prospectos
    cursos = Evento.objects.filter(Activo = True)
    # eventos = Evento.objects.all()
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
    NewCursoForm = CursoForm()
    #Pide el metodo post
    if request.method == 'POST':
        NewCursoForm = CursoForm(request.POST or None)
        #Valida la forma, la guarda y redirecciona
        if NewCursoForm.is_valid():
            curso = NewCursoForm.save(commit=False)
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
                'NewCursoForm': NewCursoForm,
                'titulo': 'Registrar un Curso',
            }
            return render(request, 'eventos/crear_curso.html', context)
    context = {
        'NewCursoForm': NewCursoForm,
        'titulo': 'Registrar un Curso',
    }
    return render(request, 'eventos/crear_curso.html', context)

#US 35
@login_required
@group_required('vendedora','administrador')
def eliminar_curso(request, id):
    curso = Evento.objects.get(id=id)
    grupos = Curso.objects.filter(Evento_id=id).count()
    # print(id)
    # print(curso)

    if(grupos > 0):
        curso.Activo = False
        evecursonto.save()
        # print(evento.Activo)
        return redirect('eventos:lista_cursos')
    else:
        curso.delete()
        return redirect('eventos:lista_cursos')

#US 33
@login_required
@group_required('vendedora','administrador')
def editar_curso(request, id):
    #Obtener el id del evento, hacer nueva forma del evento
    id_curso = Evento.objects.get(id=id)
    NewCursoForm = CursoForm(instance=id_curso)
    if request.method == 'POST':
        NewCursoForm = CursoForm(request.POST or None, instance=id_curso)
        #Si es válida, instanciar nueva empresa Y guardarla
        if NewCursoForm.is_valid():
            curso = NewCursoForm.save(commit=False)
            curso.Activo = True
            curso.save()
            messages.success(request, 'El curso ha sido actualizado.')
            return redirect('eventos:lista_evento')
        else:
            #Si no es válida, notificar al usuario
            messages.success(request, 'Existe una falla en los campos.')
            context = {
                'NewCursoForm': NewCursoForm,
                'curso': id_curso,
                'titulo': 'Editar Curso',
            }
            return render(request, 'eventos/crear_curso.html', context)
    context = {
        'NewCursoForm': NewCursoForm,
        'curso': id_curso,
        'titulo': 'Editar Curso',
    }
    return render(request, 'eventos/crear_curso.html', context)
