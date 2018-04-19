from django.shortcuts import render, redirect, reverse
from .models import Cliente, Empresa, Prospecto, Lugar, Actividad, ProspectoGrupo, Grupo, Pago
# from grupos.models import Grupo
from tablib import Dataset
import datetime
from django.db.utils import IntegrityError
from django.views import generic
from .forms import FormaActividad, ClienteForm, EmpresaForm, ProspectoForm, LugarForm, ProspectoEventoForm, ProspectoEventoEdit, PagoForm, InscribirEmpresaForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from CADHU.decorators import group_required
from django.contrib import messages
from django.urls import reverse
from django.http import *
from django.utils.timezone import now
import os
from django.conf import settings


# US43
@login_required
@group_required('vendedora','administrador')
def carga_masiva(request):
    if request.method == 'POST':
        # Guarda el archivo csv mandando por POST y lo guarda como un DataSet
        dataset = Dataset()
        resultado = []
        nuevos_prospectos = request.FILES['archivo']
        imported_data = dataset.load(nuevos_prospectos.read().decode('utf-8'), format='csv')

        # por cada fila del excel llena ...
        for i in range(0, imported_data.height):
            resultado.append('')
            # Intenta crear un lugar A partir de csv o obtener un lugar ya existente (Para no guardar repetidos)
            try:
                lugar, created = Lugar.objects.get_or_create(
                    Calle=imported_data['Calle'][i],
                    Numero_Interior=imported_data['Numero interior'][i],
                    Numero_Exterior=imported_data['Numero exterior'][i],
                    Colonia=imported_data['Colonia'][i],
                    Ciudad=imported_data['Ciudad'][i],
                    Estado=imported_data['Estado'][i],
                    Pais=imported_data['Pais'][i],
                    Codigo_Postal=imported_data['Codigo postal'][i],
                )
                try:
                    # Busca en la base de datos por si existe este prospecto para solo crear la relacion
                    prospecto = Prospecto.objects.get_or_create(
                        Nombre=imported_data['Nombre'][i],
                        Apellidos=imported_data['Apellidos'][i],
                        Email=imported_data['Email'][i],
                        Telefono_Casa=imported_data['Telefono casa'][i],
                        Telefono_Celular=imported_data['Telefono celular'][i],
                        Metodo_Captacion=imported_data['Metodo captacion'][i],
                        Estado_Civil=imported_data['Estado civil'][i],
                        Ocupacion=imported_data['Ocupacion'][i],
                        Hijos=int(imported_data['Hijos'][i]),
                        Recomendacion=imported_data['Recomendacion'][i],
                        Direccion=lugar,
                        activo=True,
                    )
                    if prospecto[1]:
                        resultado[i] = 'El prospecto se creó con éxito '
                    else:
                        resultado[i] = 'El prospecto ya existía '
                    # obtiene el curso
                    try:
                        curso = Grupo.objects.get(id=imported_data['ID curso'][i])
                        if curso:
                            # crea la relacion
                            prospectoEvento = ProspectoGrupo.objects.get_or_create(
                                Prospecto=prospecto[0],
                                Curso=curso,
                                Fecha=datetime.datetime.now().date(),
                                Interes='BAJO',
                                FlagCADHU=False,
                            )
                            if prospectoEvento[1]:
                                resultado[i] += ' y se relacionó con el curso: ' + curso.Nombre
                            else:
                                resultado[i] += ' ya existía la relación con el curso: ' + curso.Nombre
                    except Grupo.DoesNotExist:
                        resultado[i] += ' y no existe este curso.'
                except IntegrityError:
                    resultado[i] = 'Hubo un error al subir este prospecto, revisar información y buscar repetidos en el sistema'
            except:
                resultado[i] = ''
        # escribe el resultado en ultima columna del excel
        dataset.append_col(resultado, header='Estado')
        with open('static/files/resultado.xls', 'wb') as f:
            f.write(dataset.export('xls'))
            f.close()
        messages.error(request, 'La carga masiva ha sido exitosa')
        return HttpResponseRedirect(reverse('prospectos:lista_prospectos'))


# US38
@login_required
@group_required('vendedora','administrador')
def lista_clientes(request):
    # Tomar los  los clientes de la base de datos
    clientes = Cliente.objects.filter(activo=True).order_by('Fecha')
    context = {
        'clientes':clientes,
        'titulo': 'Clientes',
        'estatus': 'activo',
        }
    # Desplegar la página de clientes con enlistados con la información de la base de datos
    return render(request, 'clientes/clientes.html', context)


# US30
@login_required
@group_required('vendedora','administrador')
def eliminar_cliente(request, id):
    # Seleccionar el cliente y sus pagos de la base de datos
    cliente = Cliente.objects.get(id=id)
    pagos=Pago.objects.filter(prospecto_evento=cliente.ProspectoEvento)
    # Eliminar el cliente selecciondo
    cliente.delete()
    # Eliminar los pagos del cliente
    for pago in pagos:
         pago.delete()
    clientes = Cliente.objects.filter(activo=True).order_by('Fecha')
    context = {
        'clientes':clientes,
        'titulo': 'Clientes',
        'estatus': 'activo',
        }
    # Desplegar la lista de clientes actualizada
    return render(request, 'clientes/clientes.html', context)


# US31
@login_required
@group_required('vendedora','administrador')
def crear_cliente(request, id):
    NewClienteForm = ClienteForm()
    NewLugarForm = LugarForm()
    #Si el método HTTP es post procesar la información de la forma:
    if request.method == "POST":
        #Crear y llenar la forma
        Error = 'Forma invalida, favor de revisar sus respuestas de nuevo'
        NewClienteForm = ClienteForm(request.POST)
        NewLugarForm = LugarForm(request.POST)
        pago = Pago.objects.get(id=id)
        fecha = pago.fecha
        prospectoevento = ProspectoGrupo.objects.get(pk=pago.prospecto_evento_id)
        #Si la forma es válida guardar la información en la base de datos:
        if NewClienteForm.is_valid():
            lugar = NewLugarForm.save()
            cliente = NewClienteForm.save(commit=False)
            cliente.ProspectoEvento = prospectoevento
            cliente.Fecha = fecha
            cliente.direccionFacturacion = lugar
            prospectoevento.status = 'CURSANDO'
            prospectoevento.save()
            cliente.save()
            clientes = Cliente.objects.all()
            prospectoevento = ProspectoGrupo.objects.get(id = pago.prospecto_evento_id)
            return redirect('prospectos:lista_pagos', idPE = prospectoevento.id)
        #Si la forma es inválida mostrar el error y volver a crear la form para llenarla de nuevo
        messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
        context = {
            'Error': Error,
            'NewClienteForm': NewClienteForm,
            'NewLugarForm': NewLugarForm,
            'titulo': 'Registrar un Cliente',
        }
        return render(request, 'clientes/crear_cliente.html', context)
    #Si el método HTTP no es post, volver a enviar la forma:
    context = {
        'NewClienteForm': NewClienteForm,
        'NewLugarForm': NewLugarForm,
        'titulo': 'Registrar Cliente',
    }
    return render(request, 'clientes/crear_cliente.html', context)


# US37
@login_required
@group_required('vendedora','administrador')
def editar_cliente(request, id):
    prospectoEvento = ProspectoGrupo.objects.get(id=id)
    idcliente = Cliente.objects.get(ProspectoEvento=prospectoEvento)
    newClienteForm = ClienteForm(instance=idcliente)
    newLugarForm = LugarForm(instance=idcliente.direccionFacturacion)
    #Si el método HTTP es post procesar la información de la forma:
    if request.method == "POST":
        #Crear y llenar la forma
        Error = 'Forma invalida, favor de revisar sus respuestas de nuevo'
        newClienteForm = ClienteForm(request.POST or None, instance=idcliente)
        newLugarForm = LugarForm(request.POST or None, instance=idcliente.direccionFacturacion)
        pago = Pago.objects.filter(prospecto_evento=prospectoEvento).order_by('fecha')
        fecha = pago[0].fecha
        #Si la forma es válida guardar la información en la base de datos:
        if newClienteForm.is_valid():
            lugar = newLugarForm.save()
            cliente = newClienteForm.save(commit=False)
            cliente.ProspectoEvento = prospectoEvento
            cliente.Fecha = fecha
            cliente.direccionFacturacion = lugar
            prospectoEvento.status = 'CURSANDO'
            prospectoEvento.save()
            cliente.save()
            clientes = Cliente.objects.all()
            return redirect('prospectos:lista_pagos', idPE=prospectoEvento.id)
        #Si la forma es inválida mostrar el error y volver a crear la form para llenarla de nuevo
        messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
        context = {
            'Error': Error,
            'NewClienteForm': newClienteForm,
            'NewLugarForm': newLugarForm,
            'titulo': 'Editar Cliente',
        }
        return render(request, 'clientes/crear_cliente.html', context)
    #Si el método HTTP no es post, volver a enviar la forma:
    context = {
        'NewClienteForm': newClienteForm,
        'NewLugarForm': newLugarForm,
        'titulo': 'Editar Cliente',
    }
    return render(request, 'clientes/crear_cliente.html', context)


#US38
@login_required
@group_required('vendedora','administrador')
def info_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    lugar = Lugar.objects.get(id=cliente.direccionFacturacion.id)
    relacion = ProspectoGrupo.objects.get(id=cliente.ProspectoEvento.id)
    prospecto = Prospecto.objects.get(id=relacion.Prospecto.id)
    context = {
        'cliente': cliente,
        'lugar': lugar,
        'relacion': relacion,
        'prospecto': prospecto,
        'titulo': prospecto.Nombre,
    }
    return render(request, 'clientes/info_cliente.html', context)


#US3
@login_required
@group_required('vendedora','administrador')
def crear_prospecto(request):
    newProspectoForm = ProspectoForm(prefix='NewProspectoForm')
    newLugarForm = LugarForm(prefix='NewLugarForm')

    #Si es petición POST, procesar la información de la forma
    if request.method == 'POST':

        #Crear la instancia de la forma y llenarla con los datos
        newProspectoForm = ProspectoForm(request.POST, prefix='NewProspectoForm')
        newLugarForm = LugarForm(request.POST, prefix='NewLugarForm')

        # Validar la forma y guardar en BD
        if newProspectoForm.is_valid() and newLugarForm.is_valid():

            lugar = newLugarForm.save()
            Prospecto = newProspectoForm.save(commit=False)
            Prospecto.Direccion = lugar
            Prospecto.Usuario = request.user
            Prospecto.Fecha_Creacion = now()
            Prospecto.save()
            messages.success(request, 'El prospecto ha sido creado exitosamente')
            return redirect('prospectos:registrar_cursos', id=Prospecto.id)
        #Si la forma no es válida, volverla a mandar
        messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
        context = {
            'newProspectoForm': newProspectoForm,
            'newLugarForm': newLugarForm,
            'titulo': 'Registrar un Prospecto',
        }
        return render(request, 'prospectos/prospectos_form.html', context)

    #Si no es POST, volverla a mandar
    context = {
        'newProspectoForm': newProspectoForm,
        'newLugarForm': newLugarForm,
        'titulo': 'Registrar un Prospecto',
    }
    return render(request, 'prospectos/prospectos_form.html', context)


# US4
@login_required
@group_required('vendedora','administrador')
def editar_prospecto(request, id):
    idprospecto = Prospecto.objects.get(id=id)
    newProspectoForm = ProspectoForm(instance=idprospecto)
    newLugarForm = LugarForm(instance=idprospecto.Direccion)

    if request.method == 'POST':
        newProspectoForm = ProspectoForm(request.POST or None, instance=idprospecto)
        newLugarForm = LugarForm(request.POST or None, instance=idprospecto.Direccion)
        if newProspectoForm.is_valid() and newLugarForm.is_valid():

            prospecto = newProspectoForm.save(commit=False)
            lugar = newLugarForm.save()
            prospecto.Direccion =lugar
            prospecto.save()
            messages.success(request, 'El prospecto ha sido actualizado.')
            return redirect('prospectos:registrar_cursos', id=prospecto.id)

        else:
            messages.success(request, 'Existe una falla en los campos.')
            context = {
                'newProspectoForm': newProspectoForm,
                'newLugarForm': newLugarForm,
                'prospecto': idprospecto,
                'titulo': 'Editar Prospecto',
            }
            return render(request, 'prospectos/prospectos_form.html', context)

    context = {
        'newProspectoForm': newProspectoForm,
        'newLugarForm': newLugarForm,
        'prospecto': idprospecto,
        'titulo': 'Editar Prospecto',
    }
    return render(request, 'prospectos/prospectos_form.html', context)

# US39
@login_required
@group_required('administrador')
def baja_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    if cliente.activo:
        cliente.activo = False
        cliente.save()
        return redirect(reverse('prospectos:lista_prospectos'))
    else:
        cliente.activo = True
        cliente.save()
        return redirect(reverse('prospectos:lista_prospectos_inactivos'))

# US39
@login_required
@group_required('vendedora','administrador')
def lista_clientes_inactivos(request):
    # Tomar los  los clientes inactivos de la base
    cliente_inactivo = Cliente.objects.filter(activo=False).order_by('Fecha')
    context = {
        'cliente':cliente_inactivo,
        'titulo': 'Clientes',
        }
    # Desplegar la página de cliente con enlistados con la información de la base de datos
    return render(request, 'clientes/clientes.html', context)

# US26
@login_required
@group_required('vendedora','administrador')
def registrar_cursos(request, id):
    newProspectoEventoForm = ProspectoEventoForm()
    prospecto = Prospecto.objects.get(id=id)
    cursos = ProspectoGrupo.objects.filter(Prospecto=prospecto)

    # Si es petición POST, procesar la información de la forma
    if request.method == 'POST':

        # Crear la instancia de la forma y llenarla con los datos
        newProspectoEventoForm = ProspectoEventoForm(request.POST)

        # Validar la forma
        if newProspectoEventoForm.is_valid():
            PE = newProspectoEventoForm.save(commit=False)
            # Validar que no se este agregando un curso repetido
            try:
                ProspectoGrupo.objects.get(Prospecto=prospecto, Curso=PE.Curso)
                messages.success(request, 'El curso que quiere asignar ya ha sido asignado')
                context = {
                    'prospecto': prospecto,
                    'newProspectoEventoForm': newProspectoEventoForm,
                    'titulo': 'Registrar Registrar Grupos - ' + prospecto.Nombre + ' ' + prospecto.Apellidos,
                    'grupos': cursos,
                }
                return render(request, 'grupos/prospectoevento_form.html', context)

            #Guardar la forma en la BD
            except ProspectoGrupo.DoesNotExist:
                PE.Prospecto = prospecto
                PE.FlagCADHU = False
                PE.Fecha = now()
                PE.save()
                messages.success(request, 'Grupo asignado a prospecto')
                context = {
                    'prospecto': prospecto,
                    'newProspectoEventoForm': newProspectoEventoForm,
                    'titulo': 'Registrar Grupos - ' + prospecto.Nombre + ' ' + prospecto.Apellidos,
                    'grupos': cursos,
                }
                return render(request, 'grupos/prospectoevento_form.html', context)

        messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
    context = {
        'prospecto': prospecto,
        'newProspectoEventoForm': newProspectoEventoForm,
        'titulo': 'Registrar Grupos - ' + prospecto.Nombre + ' ' + prospecto.Apellidos,
        'grupos': cursos,
    }
    return render(request, 'grupos/prospectoevento_form.html', context)


# US11
@login_required
@group_required('vendedora','administrador')
def editar_curso(request, id):
    oldProspectoEventoForm = ProspectoEventoForm()
    cursoEditar = ProspectoGrupo.objects.get(id=id)
    newProspectoEventoForm = ProspectoEventoEdit(instance=cursoEditar)
    prospecto = cursoEditar.Prospecto
    cursos = ProspectoGrupo.objects.filter(Prospecto=prospecto)
    # Si es petición POST, procesar la información de la forma
    if request.method == 'POST':
        # Crear la instancia de la forma y llenarla con los datos
        newProspectoEventoForm = ProspectoEventoEdit(request.POST or None, instance=cursoEditar)
        # Validar la forma y guardarla en la BD
        if newProspectoEventoForm.is_valid():
            PE = newProspectoEventoForm.save(commit=False)
            PE.Prospecto = prospecto
            PE.Curso = cursoEditar.Curso
            PE.save()
            messages.success(request, 'Grupo Modificado a prospecto')
            context = {
                'prospecto': prospecto,
                'newProspectoEventoForm': oldProspectoEventoForm,
                'titulo': 'Registrar Grupos - ' + prospecto.Nombre + ' ' + prospecto.Apellidos,
                'grupos': cursos,
            }
            return render(request, 'grupos/prospectoevento_form.html', context)
        messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
    context = {
        'prospecto': prospecto,
        'newProspectoEventoForm': newProspectoEventoForm,
        'titulo': 'Editar Grupo - ' + cursoEditar.Curso.Nombre,
        'grupos': cursos,
    }
    return render(request, 'grupos/prospectoevento_edit.html', context)


# US10
@login_required
@group_required('vendedora','administrador')
def eliminar_curso(request, id):
    curso = ProspectoGrupo.objects.get(id=id)
    newProspectoEventoForm = ProspectoEventoForm()
    prospecto = curso.Prospecto
    cursos = ProspectoGrupo.objects.filter(Prospecto=prospecto)
    if(Pago.objects.filter(prospecto_evento=curso).count()>0):
        messages.success(request, 'El prospecto ya ha realizado un pago, por ende, el curso no puede ser eliminado')
        context = {
            'prospecto': prospecto,
            'newProspectoEventoForm': newProspectoEventoForm,
            'titulo': 'Registrar Grupo - ' + prospecto.Nombre + ' ' + prospecto.Apellidos,
            'grupos': cursos,
        }
        return render(request, 'grupos/prospectoevento_form.html', context)
    else:
        curso.delete()
        messages.success(request, 'Grupo eliminado de manera exitosa')
        context = {
            'prospecto': prospecto,
            'newProspectoEventoForm': newProspectoEventoForm,
            'titulo': 'Registrar Grupo - ' + prospecto.Nombre + ' ' + prospecto.Apellidos,
            'grupos': cursos,
        }
        return render(request, 'grupos/prospectoevento_form.html', context)


# US23
@login_required
@group_required('vendedora', 'administrador')
def info_prospecto_grupo(request, rel):
    relacion = ProspectoGrupo.objects.get(id=rel)
    prospecto = Prospecto.objects.get(id=relacion.prospecto.id)
    titulo = relacion.grupo
    context = {
        'relacion': relacion,
        'actividades': relacion.actividad_set.all(),
        'prospecto': prospecto,
        'titulo': titulo,
    }
    return render(request, 'grupos/info_prospectocurso.html', context)


# US7
@login_required
@group_required('vendedora', 'administrador')
def lista_prospectos(request):
    # Tomar los  los prospectos de la base
    #prospectos = Prospecto.objects.all()
    prostpecto_activo = Prospecto.objects.filter(activo=True)
    context = {
        'prospectos':prostpecto_activo,
        'titulo': 'Prospectos',
        }
    # Desplegar la página de prospectos con enlistados con la información de la base de datos
    return render(request, 'prospectos/prospectos.html', context)

# US6
@login_required
@group_required('vendedora','administrador')
def lista_prospectos_inactivo(request):
    # Tomar los  los prospectos de la base
    # prospectos = Prospecto.objects.all()
    prostpecto_inactivo = Prospecto.objects.filter(activo=False)
    context = {
        'prospectos':prostpecto_inactivo,
        'titulo': 'Prospectos inactivos',
        }
    # Desplegar la página de prospectos con enlistados con la información de la base de datos
    return render(request, 'prospectos/prospectos.html', context)

# US6
@login_required
@group_required('vendedora','administrador')
def baja_prospecto(request, id):
    # Obtener el prospecto
    prospecto = Prospecto.objects.get(id=id)
    # Si el prospecto es activo, cambiarlo a inactivo
    if prospecto.activo:
        prospecto.activo = False
        prospecto.save()
        return redirect(reverse('prospectos:lista_prospectos'))
    # Si el prospecto es activo, guardarlo
    else:
        prospecto.activo = True
        prospecto.save()
        return redirect(reverse('prospectos:lista_prospectos_inactivo'))

# US5
@login_required
@group_required('vendedora', 'administrador')
def info_prospecto(request, id):
    newProspectoEventoForm = ProspectoEventoForm()
    prospecto = Prospecto.objects.get(id=id)
    cursos = ProspectoGrupo.objects.filter(Prospecto=prospecto)
    actividades = Actividad.objects.filter(prospecto_evento__Prospecto=prospecto).order_by('fecha', 'hora')
    titulo = 'Información de prospecto'
    agenda = []
    bitacora = []
    for actividad in actividades:
        if not actividad.terminado:
            agenda.append(actividad)
        else:
            bitacora.append(actividad)
    if request.method == 'POST':
        # Crear la instancia de la forma y llenarla con los datos
        newProspectoEventoForm = ProspectoEventoForm(request.POST)
        # Validar la forma
        if newProspectoEventoForm.is_valid():
            PE = newProspectoEventoForm.save(commit=False)
            # Validar que no se este agregando un curso repetido
            try:
                ProspectoGrupo.objects.get(Prospecto=prospecto, Curso=PE.Curso)
                messages.success(request, 'El curso que quiere asignar ya ha sido asignado')
                context = {
                    'prospecto': prospecto,
                    'newProspectoEventoForm': newProspectoEventoForm,
                    'titulo': titulo,
                    'actividades': actividades,
                    'agenda': agenda,
                    'bitacora': bitacora,
                    'grupos': cursos,
                }
                return render(request, 'prospectos/info_prospecto.html', context)
            # Guardar la forma en la BD
            except ProspectoGrupo.DoesNotExist:
                PE.Prospecto = prospecto
                PE.FlagCADHU = False
                PE.Fecha = now()
                PE.save()
                messages.success(request, 'Grupo asignado a prospecto')
                context = {
                    'prospecto': prospecto,
                    'newProspectoEventoForm': newProspectoEventoForm,
                    'actividades': actividades,
                    'agenda': agenda,
                    'bitacora': bitacora,
                    'titulo': titulo,
                    'grupos': cursos,
                }
                return render(request, 'prospectos/info_prospecto.html', context)
        messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
    context = {
        'titulo': titulo,
        'newProspectoEventoForm': newProspectoEventoForm,
        'actividades': actividades,
        'agenda': agenda,
        'bitacora': bitacora,
        'grupos': cursos,
        'prospecto': prospecto,
    }
    return render(request, 'prospectos/info_prospecto.html', context)

# US17
@login_required
@group_required('vendedora','administrador')
def lista_empresas(request):
    # Si las empresas son activas, desplegarlas
    empresas = Empresa.objects.filter(activo=True)
    context = {
        'empresas':empresas,
        'titulo': 'Empresas',
        'estatus': 'activo',
        }
    return render(request, 'empresas/empresas.html', context)

@login_required
@group_required('vendedora','administrador')
def lista_empresas_inactivo(request):
    # Tomar los  los empresas de la base inactivos
    empresa_inactivo = Empresa.objects.filter(activo=False)
    context = {
        'empresas':empresa_inactivo,
        'titulo': 'Empresas inactivas',
        'estatus': 'inactivo',
        }
    # Desplegar la página de empresas con enlistados con la información de la base de datos
    return render(request, 'empresas/empresas.html', context)


#US14
@login_required
@group_required('vendedora','administrador')
def editar_empresa(request, id):
    #Obtener el id de la empresa, hacer nueva forma de la empresa y de lugar
    idempresa = Empresa.objects.get(id=id)
    NewEmpresaForm = EmpresaForm(instance=idempresa)
    NewLugarForm = LugarForm(instance=idempresa.Direccion)
    if request.method == 'POST':
        NewEmpresaForm = EmpresaForm(request.POST or None, instance=idempresa)
        NewLugarForm = LugarForm(request.POST or None, instance=idempresa.Direccion)
        #Si es válida, instanciar nueva empresa Y guardarla
        if NewEmpresaForm.is_valid() and NewLugarForm.is_valid():
            empresa = NewEmpresaForm.save(commit=False)
            lugar = NewLugarForm.save()
            empresa.Direccion = lugar
            empresa.save()
            messages.success(request, 'La empresa ha sido actualizada.')
            return redirect('prospectos:lista_empresas')
        else:
            #Si no es válida, notificar al usuario
            messages.success(request, 'Existe una falla en los campos.')
            context = {
                'NewEmpresaForm': NewEmpresaForm,
                'NewLugarForm': NewLugarForm,
                'empresa': idempresa,
                'titulo': 'Editar Empresa',
            }
            return render(request, 'empresas/empresas_form.html', context)
    context = {
        'NewEmpresaForm': NewEmpresaForm,
        'NewLugarForm': NewLugarForm,
        'empresa': idempresa,
        'titulo': 'Editar Empresa',
    }
    return render(request, 'empresas/empresas_form.html', context)

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
            return lista_empresas(request)
        #Si la forma es inválida mostrar el error y volver a crear la form para llenarla de nuevo
        messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
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
def empresa_info(request, id):
    empresa = Empresa.objects.get(id=id)
    prospectos = Prospecto.objects.filter(Empresa=empresa)
    lugar = Lugar.objects.get(id=empresa.Direccion.id)
    context = {
        'empresa': empresa,
        'prospectos': prospectos,
        'lugar': lugar,
        'titulo': empresa.nombre,
    }
    return render(request, 'empresas/empresas_info.html', context)

# US16 y US18
@login_required
@group_required('vendedora','administrador')
def baja_empresas(request, id):
    # Obtener empresa
    empresa = Empresa.objects.get(id=id)
    # Si la empresa es activa, inactivarla
    if empresa.activo:
        empresa.activo = False
        empresa.save()
        return redirect(reverse('prospectos:lista_empresas'))
    # Si la empresa es activa, guardarla
    else:
        empresa.activo = True
        empresa.save()
        return redirect(reverse('prospectos:lista_empresas_inactivo'))


# US19
@login_required
@group_required('vendedora','administrador')
def inscribir_empresa(request, id):
    empresa = Empresa.objects.get(id=id)
    prospectos = Prospecto.objects.exclude(Empresa__isnull=False) | Prospecto.objects.filter(Empresa=empresa)
    if request.method == "POST":
        vaciar = Prospecto.objects.filter(Empresa=empresa)
        for va in vaciar:
            va.Empresa= None
            va.save()
        for algo in request.POST.getlist('prospectos[]'):
            prospect = Prospecto.objects.get(id=algo)
            prospect.Empresa= empresa
            prospect.save()
        return empresa_info(request,id)
    context = {
            'prospectos':prospectos,
            'empresa':empresa,
            'titulo': 'Asignar prospectos a: '+empresa.nombre,
        }
    return render(request, 'empresas/empresa_prospectos_form.html', context)


# US15
@login_required
@group_required('vendedora','administrador')
def lista_actividades(request, pk):
    # Mostrar todas las empresas
    actividades = Actividad.objects.filter(prospecto_grupo=pk)
    context = {
        'actividades': actividades,
        'id': pk
        }
    return render(request, 'actividades/actividades.html', context)


# US12
@login_required
@group_required('vendedora', 'administrador')
def crear_actividad(request, pk):
    new_actividad_form = FormaActividad()
    # SI HAY UNA FORMA ENVIADA EN POST
    if request.method == 'POST':
        new_actividad_form = FormaActividad(request.POST)
        prospecto_grupo = ProspectoGrupo.objects.get(id=pk)
        # SI LA FORMA ES VÁLIDA
        if new_actividad_form.is_valid():
            actividad = new_actividad_form.save(commit=False)
            # SE GUARDA LA NOTA
            actividad.prospecto_grupo = prospecto_grupo
            actividad.save()
            # Mensaje éxito
            messages.success(request, 'La actividad ha sido agregada')
            return info_prospecto_grupo(request, pk)
        else:
            # Mensaje error
            error = 'Forma inválida'
            messages.success(request, 'Forma inválida')
            context = {
                'Error': error,
                'form': new_actividad_form,
                'titulo': 'Agregar actividad',
                'id': id
            }
            return render(request, 'actividades/crear_actividad.html', context)
    # CARGAR LA VISTA
    context = {
        'form': new_actividad_form,
        'titulo': 'Agregar actividad',
        'id': pk
    }
    return render(request, 'actividades/crear_actividad.html', context)


# US12
@login_required
@group_required('vendedora','administrador')
def estado_actividad(request, id):
    act = Actividad.objects.get(id=id)
    if act.terminado:
        act.terminado = False
        act.save()
    else:
        act.terminado = True
        act.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# US12
@login_required
@group_required('vendedora','administrador')
def estado_flag(request, id):
    rel = ProspectoGrupo.objects.get(id=id)
    if rel.FlagCADHU:
        rel.FlagCADHU = False
        rel.save()
    else:
        rel.FlagCADHU = True
        rel.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# US41
@login_required
@group_required('administrador')
def nuevo_pago(request, idPE):
    # recibir forma
    forma_pago = PagoForm()
    # si se recibe una forma con post
    if request.method == 'POST':
        # print("entró")
        Forma_nuevo_pago = PagoForm(request.POST)
        # si la forma es válida
        if Forma_nuevo_pago.is_valid():
            # print(Forma_nuevo_pago)
            #VALIDAR QUE EL PAGO NO SUPERE EL MONTO MÁXIMO
            # if(total_pagos + float(request.POST['monto']) <= curso.Costo):
            # se guarda la forma
            pago = Forma_nuevo_pago.save(commit=False)
            pago.prospecto_evento_id = idPE
            pago = Forma_nuevo_pago.save()
            # se redirige a la próxima vista
            messages.success(request, 'Pago agregado exitosamente!')
            pagos = Pago.objects.filter(prospecto_evento_id = idPE).count()
            if(pagos > 1):
                # print(idPE)
                # print(pago.id)
                pe = ProspectoGrupo.objects.get(id = idPE)
                return redirect('prospectos:lista_pagos', idPE=idPE)
            else:
                return redirect('prospectos:crear_cliente', id=pago.id)
        else:
        # se renderea la forma nuevamente con los errores marcados
            context = {
                'form': Forma_nuevo_pago,
                'titulo': 'Agregar Pago',
                'error_message': Forma_nuevo_pago.errors
            }
            return render(request, 'pagos/nuevo_pago.html', context)
    else:
        total_pagos = 0
        query_pagos = Pago.objects.filter(prospecto_evento_id = idPE)
        for pago in query_pagos:
            total_pagos += pago.monto
        pe = ProspectoGrupo.objects.get(id = idPE)
        curso = Grupo.objects.get(id = pe.Curso_id)
        #VALIDAR QUE EL PAGO NO SUPERE EL MONTO MÁXIMO
        monto_maximo = curso.Costo - total_pagos
        # se renderea la página
        context = {
            'form': forma_pago,
            'titulo': 'Agregar Pago',
            'monto_maximo': monto_maximo,
        # 'grupos': Evento.objects.all().order_by('Nombre')
        }
        return render(request, 'pagos/nuevo_pago.html', context)

# US42
@login_required
@group_required('administrador')
def lista_pagos(request, idPE):
    # prospecto_grupo = ProspectoGrupo.objects.get(id = idPE)
    pagos = Pago.objects.filter(prospecto_evento_id=idPE).count()
    pe = ProspectoGrupo.objects.get(id=idPE)
    # print(pe.Curso_id)
    total_pagos = 0
    pagos2 = Pago.objects.filter(prospecto_evento_id=idPE)
    for pago in pagos2:
        total_pagos += pago.monto
    curso = Grupo.objects.get(id = pe.Curso_id)
    if(pagos > 0):
        context = {
            'titulo': 'Lista de Pagos',
            'prospecto': Prospecto.objects.get(id=pe.Prospecto.id),
            'pagos': Pago.objects.filter(prospecto_evento=pe).order_by('fecha'),
            'cliente': Cliente.objects.get(ProspectoEvento=pe),
            'idPE': idPE,
            'curso': curso,
            'subtotal': total_pagos,
            'restante': curso.Costo - total_pagos,
        }
        return render(request, 'pagos/lista_pagos.html', context)
    else:
        return redirect('prospectos:nuevo_pago', idPE = idPE)

# US42
@login_required
@group_required('administrador')
def autorizar_pago(request, id):
    pago = Pago.objects.get(id=id)
    if pago.validado == False:
        pago.validado = True
        pago.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
