from django.shortcuts import render, redirect
from .models import Empresa, Prospecto, Lugar, Actividad
from datetime import time
from django.views import generic
from .forms import FormaActividad, EmpresaForm, ProspectoForm, LugarForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from CADHU.decorators import group_required
from django.contrib import messages
from django.urls import reverse


@login_required
@group_required('vendedora','administrador')
def lista_prospectos(request):
    prospectos = Prospecto.objects.all()
    context = {
        'prospectos':prospectos,
        'titulo': 'Prospectos',
        }
    return render(request, 'prospectos/prospectos.html', context)

@login_required
@group_required('vendedora','administrador')
def lista_empresa(request):
    empresas = Empresa.objects.all()
    context = {
        'empresas':empresas
        }
    return render(request, 'empresas/empresas.html', context)

@login_required
@group_required('vendedora','administrador')
def crear_prospecto(request):
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
            return redirect('prospectos:lista_prospectos')

        context = {
            'NewProspectoForm': NewProspectoForm,
            'NewLugarForm': NewLugarForm,
            'titulo': 'Registrar un Prospecto',
        }
        return render(request, 'prospectos/prospectos_form.html', context)
    context = {
        'NewProspectoForm': NewProspectoForm,
        'NewLugarForm': NewLugarForm,
        'titulo': 'Registrar un Prospecto',
    }
    return render(request, 'prospectos/prospectos_form.html', context)


@login_required
@group_required('vendedora','administrador')
def editar_prospecto(request, id):
    idprospecto = Prospecto.objects.get(id=id)
    NewProspectoForm = ProspectoForm(instance=idprospecto)
    NewLugarForm = LugarForm(instance=idprospecto.Direccion)

    if request.method == 'POST':
        NewProspectoForm = ProspectoForm(request.POST or None, instance=idprospecto)
        NewLugarForm = LugarForm(request.POST or None, instance=idprospecto.Direccion)
        if NewProspectoForm.is_valid() and NewLugarForm.is_valid():

            prospecto = NewProspectoForm.save(commit=False)
            Lugar = NewLugarForm.save()
            Prospecto.Direccion =Lugar
            prospecto.save()
            messages.success(request, 'El prospecto ha sido actualizado.')
            return redirect('prospectos:lista_prospectos')

        else:
            messages.success(request, 'Existe una falla en los campos.')
            context = {
                'NewProspectoForm': NewProspectoForm,
                'NewLugarForm': NewLugarForm,
                'prospecto': idprospecto,
                'titulo': 'Editar Prospecto',
            }
            return render(request, 'prospectos/prospectos_form.html', context)

    context = {
        'NewProspectoForm': NewProspectoForm,
        'NewLugarForm': NewLugarForm,
        'prospecto': idprospecto,
        'titulo': 'Editar Prospecto',
    }
    return render(request, 'prospectos/prospectos_form.html', context)


# US13
@login_required
@group_required('vendedora','administrador')
def crear_empresa(request):
    NewEmpresaForm = EmpresaForm()
    NewLugarForm = LugarForm()
    #Si el método HTTP es post procesar la información de la forma:
    if request.method == "POST":
        #Definir el error para forma invalida:
        Error = 'Forma invalida, favor de revisar sus respuestas de nuevo'
        #Crear y llenar la forma
        NewEmpresaForm = EmpresaForm(request.POST)
        NewLugarForm = LugarForm(request.POST)
        #Si la forma es válida guardar la información en la base de datos:
        if NewEmpresaForm.is_valid() and NewLugarForm.is_valid():
            Lugar = NewLugarForm.save()
            Empresa = NewEmpresaForm.save(commit=False)
            Empresa.Direccion = Lugar
            Empresa.save()
            return lista_empresa(request)
        #Si la forma es inválida mostrar el error y volver a crear la form para llenarla de nuevo
        context = {
            'Error': Error,
            'NewEmpresaForm': NewEmpresaForm,
            'NewLugarForm': NewLugarForm,
            'titulo': 'Registrar una Empresa',
        }
        return render(request, 'empresas/empresas_form.html', context)
    #Si el método HTTP no es post, volver a enviar la forma:
    context = {
        'NewEmpresaForm': NewEmpresaForm,
        'NewLugarForm': NewLugarForm,
        'titulo': 'Registrar una Empresa',
    }
    return render(request, 'empresas/empresas_form.html', context)




@login_required
@group_required('vendedora','administrador')
def lista_actividades(request,id):
    actividades = Actividad.objects.filter(prospecto_evento=id)
    context = {
        'actividades':actividades,
        'id':id
        }
    return render(request, 'actividades/actividades.html', context)


@login_required
@group_required('vendedora','administrador')
def crear_actividad(request,id):
    NewActividadForm = FormaActividad()
    if request.method == 'POST':
        NewActividadForm = FormaActividad(request.POST)
        if NewActividadForm.is_valid():
            print('jai')
            actividad = NewActividadForm.save(commit=False)
            actividad.save()
            return redirect(reverse('prospectos:lista_actividades',kwargs={'id':id}))
        else:
            print('hola')
            mensaje = ''
            context = {
                'form': NewActividadForm,
                'titulo': 'Agregar actividad',
            }
            for field, errors in NewActividadForm.errors.items():
                for error in errors:
                    mensaje += error
            context['mensaje_error'] = mensaje
            return render(request, 'actividades/crear_actividad.html', context)
    context = {
        'form': NewActividadForm,
        'titulo': 'Agregar actividad',
        'id':id
    }
    return render(request, 'actividades/crear_actividad.html', context)
