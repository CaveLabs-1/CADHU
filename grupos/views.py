from django.shortcuts import render, redirect, reverse
from .models import Grupo
from prospectos.models import ProspectoGrupo, Cliente
from .forms import FormaGrupo
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required


# US29
@login_required
@group_required('vendedora', 'administrador')
def grupos(request):
    context = {
        'titulo': 'Grupos',
        'grupos': Grupo.objects.filter(activo=True),
    }
    return render(request, 'grupos/grupos.html', context)


# US29
@login_required
@group_required('vendedora', 'administrador')
def grupos_inactivos(request):
    context = {
        'titulo': 'Grupos inactivos',
        'grupos': Grupo.objects.filter(activo=False),
    }
    return render(request, 'grupos/grupos.html', context)


# US ???
@login_required
@group_required('administrador')
def nuevo_grupo(request):
    # recibir forma
    forma_nuevo_grupo = FormaGrupo()
    # si se recibe una forma con post
    if request.method == 'POST':
        forma_nuevo_grupo = FormaGrupo(request.POST)
        # si la forma es válida
        if forma_nuevo_grupo.is_valid():
            # se guarda la forma
            forma_nuevo_grupo.save()
            # se redirige a la próxima vista
            messages.success(request, '¡Grupo agregado exitosamente!')
            return redirect('/grupos/')
        # se renderea la forma nuevamente con los errores marcados
        context = {
            'form': forma_nuevo_grupo,
            'titulo': 'Agregar Grupo',
            'error_message': forma_nuevo_grupo.errors,
            'boton': '+ Agregar Grupo',
        }
        return render(request, 'grupos/form_grupo.html', context)
    # se renderea la página
    context = {
        'form': forma_nuevo_grupo,
        'titulo': 'Agregar Grupo',
        'grupos': Grupo.objects.filter(activo=True).order_by('nombre'),
        'boton': '+ Agregar Grupo',
    }
    return render(request, 'grupos/form_grupo.html', context)


# US27
@login_required
@group_required('administrador')
def editar_grupo(request, pk):
    # Hacer asignaciones desde la BD
    grupo = Grupo.objects.get(id=pk)
    forma_grupo = FormaGrupo(instance=grupo)
    # Checar que el metodo sea POST
    if request.method == 'POST':
        forma_grupo = FormaGrupo(request.POST or None, instance=grupo)
        # Checar que la forma sea valida y guardarla
        if forma_grupo.is_valid():
            forma_grupo.save()
            messages.success(request, '¡Grupo editado exitosamente!')
            return redirect('/grupos/')
        # Si la forma no es valida, hacer render y mandar errores
        context = {
            'form': forma_grupo,
            'titulo': 'Modificar Grupo',
            'error_message': forma_grupo.errors,
            'boton': 'Modificar Grupo',
        }
        return render(request, 'grupos/form_grupo.html', context)
    # Render a la pagina
    context = {
        'form': forma_grupo,
        'titulo': 'Editar Grupo',
        'grupos': Grupo.objects.filter(activo=True).order_by('nombre'),
        'boton': 'Modificar Grupo',
    }
    return render(request, 'grupos/form_grupo.html', context)


# US 28
@login_required
@group_required('administrador')
def eliminar_grupo(request, pk):
    grupo = Grupo.objects.get(id=pk)
    grupos_utilizados = ProspectoGrupo.objects.filter(grupo=grupo).count()
    if grupo.activo:
        if grupos_utilizados > 0:
            grupo.activo = False
            grupo.save()
            return redirect('grupos:grupos')
        else:
            grupo.delete()
            return redirect('grupos:grupos')


# US25
@login_required
@group_required('administrador', 'vendedora')
def info_grupo(request, pk):
    grupo = Grupo.objects.get(id=pk)
    prospectos_lista = ProspectoGrupo.objects.filter(grupo=grupo)
    prospectos = []
    clientes = []
    for prospecto in prospectos_lista:
        if prospecto.cliente_set.exists():
            cliente = Cliente.objects.get(prospecto_grupo=prospecto.id)
            clientes.append(cliente)
        else:
            prospectos.append(prospecto)
    context = {
        'titulo': 'Información: ' + grupo.nombre,
        'grupo': grupo,
        'clientes': clientes,
        'prospectos': prospectos,
    }
    return render(request, 'grupos/info_grupo.html', context)
