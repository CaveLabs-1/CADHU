from django.shortcuts import render, redirect, reverse
from .models import Empresa, Prospecto, Lugar, Actividad, ProspectoEvento
from cursos.models import Curso
from tablib import Dataset
import datetime
from django.views import generic
from .forms import FormaActividad, EmpresaForm, ProspectoForm, LugarForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from CADHU.decorators import group_required
from django.http import HttpResponseRedirect
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


def carga_masiva(request):
    if request.method == 'POST':
        # Guarda el archivo csv mandando por POST y lo guarda como un DataSet
        dataset = Dataset()
        nuevos_prospectos = request.FILES['archivo']
        imported_data = dataset.load(nuevos_prospectos.read().decode('utf-8'), format='csv')

        # por cada fila del excel llena ...
        for i in range(1, imported_data.height):
        # Intenta crear un lugar A partir de csv o obtener un lugar ya existente (Para no guardar repetidos)
            lugar = Lugar.objects.get_or_create(
                Calle=imported_data['Calle'][i],
                Numero_Interior=imported_data['Numero interior'][i],
                Numero_Exterior=imported_data['Numero exterior'][i],
                Colonia=imported_data['Colonia'][i],
                Ciudad=imported_data['Ciudad'][i],
                Estado=imported_data['Estado'][i],
                Pais=imported_data['Pais'][i],
                Codigo_Postal=imported_data['Codigo postal'][i],
            )

            # busca la bd por si existe este prospecto para solo crear la relacion
            prospecto = Prospecto.objects.get_or_create(
                Nombre=imported_data['Nombre'][i],
                Apellido_Paterno=imported_data['Apellido paterno'][i],
                Apellido_Materno=imported_data['Apellido materno'][i],
                Email=imported_data['Email'][i],
                Telefono_Casa=imported_data['Telefono casa'][i],
                Telefono_Celular=imported_data['Telefono celular'][i],
                Metodo_Captacion=imported_data['Metodo captacion'][i],
                Estado_Civil=imported_data['Estadp civil'][i],
                Ocupacion=imported_data['Ocupacion'][i],
                Hijos=int(imported_data['Hijos'][i]),
                Recomendacion=imported_data['Recomendacion'][i],
                Direccion=lugar[0],
            )
            #Si el resultado es true significa que se creo el objeto si es false significa que ya existia
            if prospecto[1]:
                print('Si se importo esta madre')
            else:
                print('No se importo esta madre porque ya existe sacate ALV')

            # obtiene el curso
            curso = Curso.objects.get(id=imported_data['ID curso'][i])
            # crea la relacion
            prospectoEvento = ProspectoEvento.objects.get_or_create(
                Prospecto=prospecto[0],
                Curso=curso,
                Fecha=datetime.datetime.now().date(),
                Interes=('BAJO', 'BAJO'),
                FlagCADHU=False,
            )
            if prospectoEvento[1]:
                print('se crea la relacion')
            else:
                print('no se creo la relacion')





        # imported_data =dataset.load('xlsx', open(nuevos_prospectos, 'rb').read())
        # resultado = resource_prospecto.import_data(dataset, dry_run=True)
        # if not resultado.has_er rors():
        #     resource_prospecto.import_data(dataset, dry_run=False)
        #     context = {
        #         'errores': 'No hay errores',
        #     }
        #     return HttpResponseRedirect(reverse('prospectos:lista_prospectos'), context)
        # else:
        #     context = {
        #         'errores': resultado.base_errors,
        #     }
        #     return HttpResponseRedirect(reverse('prospectos:lista_prospectos'), context)


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


@login_required
@group_required('vendedora','administrador')
def empresa_crear(request):
    NewEmpresaForm = EmpresaForm()
    NewLugarForm = LugarForm()
    if request.method == "POST":
        Error = 'Forma invalida, favor de revisar sus respuestas de nuevo'
        NewEmpresaForm = EmpresaForm(request.POST)
        NewLugarForm = LugarForm(request.POST)
        if NewEmpresaForm.is_valid() and NewLugarForm.is_valid():
            Lugar = NewLugarForm.save()
            Empresa = NewEmpresaForm.save(commit=False)
            Empresa.Direccion = Lugar
            Empresa.save()
            return lista_empresa(request)
        context = {
            'Error': Error,
            'NewEmpresaForm': NewEmpresaForm,
            'NewLugarForm': NewLugarForm,
            'titulo': 'Registrar una Empresa',
        }
        return render(request, 'empresas/empresas_form.html', context)
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
@group_required('vendedora', 'administrador')
def crear_actividad(request, id):
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
        'id': id
    }
    return render(request, 'actividades/crear_actividad.html', context)
