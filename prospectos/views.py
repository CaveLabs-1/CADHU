from django.shortcuts import render, redirect, reverse
from .models import Cliente, Empresa, Prospecto, Lugar, Actividad, ProspectoEvento, Curso, Pago
# from cursos.models import Curso
from tablib import Dataset
import datetime
from django.db.utils import IntegrityError
from django.views import generic
from .forms import FormaActividad, ClienteForm, EmpresaForm, ProspectoForm, LugarForm, ProspectoEventoForm, PagoForm
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
                        Activo=True,
                    )
                    if prospecto[1]:
                        resultado[i] = 'El prospecto se creó con éxito '
                    else:
                        resultado[i] = 'El prospecto ya existía '
                    # obtiene el curso
                    try:
                        curso = Curso.objects.get(id=imported_data['ID curso'][i])
                        if curso:
                            # crea la relacion
                            prospectoEvento = ProspectoEvento.objects.get_or_create(
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
                    except Curso.DoesNotExist:
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


# US31
@login_required
@group_required('vendedora','administrador')
def crear_cliente(request, id):
    NewClienteForm = ClienteForm()
    #Si el método HTTP es post procesar la información de la forma:
    if request.method == "POST":
        #Definir el error para forma invalida:
        #Crear y llenar la forma
        NewClienteForm = ClienteForm(request.POST)
        pago = Pago.objects.get(id=id)
        fecha = pago.fecha
        prospectoevento = ProspectoEvento.objects.get(pk=pago.prospecto_evento_id)
        #Si la forma es válida guardar la información en la base de datos:
        if NewClienteForm.is_valid():
            cliente = NewClienteForm.save(commit=False)
            cliente.ProspectoEvento = prospectoevento
            cliente.Fecha = fecha
            prospectoevento.status = 'CURSANDO'
            prospectoevento.save()
            cliente.save()
            clientes = Cliente.objects.all()

            prospectoevento = ProspectoEvento.objects.get(id = pago.prospecto_evento_id)
            print(prospectoevento.Prospecto_id)
            print(prospectoevento.id)

            # context = {
            #     'id': NewClienteForm,
            #     'titulo': 'Registrar un Cliente',
            # }
            # prospecto_evento = ProspectoEvento.objects.filter(prospecto_evento_id = idPE).count()
            return redirect('prospectos:lista_pagos', id = prospectoevento.Prospecto_id, idPE = prospectoevento.id)
            # return redirect('prospectos:lista_pagos', )
        #Si la forma es inválida mostrar el error y volver a crear la form para llenarla de nuevo
        messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
        context = {
            'NewClienteForm': NewClienteForm,
            'titulo': 'Registrar un Cliente',
        }
        return render(request, 'clientes/crear_cliente.html', context)
    #Si el método HTTP no es post, volver a enviar la forma:
    context = {
        'NewClienteForm': NewClienteForm,
        'titulo': 'Registrar un Cliente',
    }
    return render(request, 'clientes/crear_cliente.html', context)


#US3
@login_required
@group_required('vendedora','administrador')
def crear_prospecto(request):
    NewProspectoForm = ProspectoForm(prefix='NewProspectoForm')
    NewLugarForm = LugarForm(prefix='NewLugarForm')

    #Si es petición POST, procesar la información de la forma
    if request.method == 'POST':

        #Crear la instancia de la forma y llenarla con los datos
        NewProspectoForm = ProspectoForm(request.POST, prefix='NewProspectoForm')
        NewLugarForm = LugarForm(request.POST, prefix='NewLugarForm')

        # Validar la forma y guardar en BD
        if NewProspectoForm.is_valid() and NewLugarForm.is_valid():

            Lugar = NewLugarForm.save()
            Prospecto = NewProspectoForm.save(commit=False)
            Prospecto.Direccion = Lugar
            Prospecto.Usuario = request.user
            Prospecto.Fecha_Creacion = now()
            Prospecto.save()
            messages.success(request, 'El prospecto ha sido creado exitosamente')
            return redirect('prospectos:registrar_cursos', id=Prospecto.id)

            #Si la forma no es válida, volverla a mandar
        messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
        context = {
            'NewProspectoForm': NewProspectoForm,
            'NewLugarForm': NewLugarForm,
            'titulo': 'Registrar un Prospecto',
        }
        return render(request, 'prospectos/prospectos_form.html', context)

    #Si no es POST, volverla a mandar
    context = {
        'NewProspectoForm': NewProspectoForm,
        'NewLugarForm': NewLugarForm,
        'titulo': 'Registrar un Prospecto',
    }
    return render(request, 'prospectos/prospectos_form.html', context)


@login_required
@group_required('vendedora','administrador')
#US4
def editar_prospecto(request, id):
    idprospecto = Prospecto.objects.get(id=id)
    NewProspectoForm = ProspectoForm(instance=idprospecto)
    NewLugarForm = LugarForm(instance=idprospecto.Direccion)

    if request.method == 'POST':
        NewProspectoForm = ProspectoForm(request.POST or None, instance=idprospecto)
        NewLugarForm = LugarForm(request.POST or None, instance=idprospecto.Direccion)
        if NewProspectoForm.is_valid() and NewLugarForm.is_valid():

            prospecto = NewProspectoForm.save(commit=False)
            lugar = NewLugarForm.save()
            prospecto.Direccion =lugar
            prospecto.save()
            messages.success(request, 'El prospecto ha sido actualizado.')
            return redirect('prospectos:registrar_cursos', id=prospecto.id)

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



#US26
def registrar_cursos(request, id):
    prospecto = Prospecto.objects.get(id=id)
    cursos = ProspectoEvento.objects.filter(Prospecto=prospecto)
    NewProspectoEventoForm = ProspectoEventoForm()

    # Si es petición POST, procesar la información de la forma
    if request.method == 'POST':

        # Crear la instancia de la forma y llenarla con los datos
        NewProspectoEventoForm = ProspectoEventoForm(request.POST)

        # Validar la forma y guardar en BD
        if NewProspectoEventoForm.is_valid():
            PE = NewProspectoEventoForm.save(commit=False)
            PE.Prospecto = prospecto
            PE.FlagCADHU = False
            PE.Fecha = now()
            PE.save()
            messages.success(request, 'Curso agregado')
            context = {
                'prospecto': prospecto,
                'NewProspectoEventoForm': NewProspectoEventoForm,
                'titulo': 'Registrar Cursos - ' + prospecto.Nombre + ' ' + prospecto.Apellidos,
                'cursos': cursos,
            }
            return render(request, 'cursos/prospectoevento_form.html', context)

    messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
    context = {
        'prospecto': prospecto,
        'NewProspectoEventoForm': NewProspectoEventoForm,
        'titulo': 'Registrar Cursos - ' + prospecto.Nombre + ' ' + prospecto.Apellidos,
        'cursos': cursos,
    }
    return render(request, 'cursos/prospectoevento_form.html', context)


#US7
@login_required
@group_required('vendedora','administrador')
def lista_prospectos(request):
    # Tomar los  los prospectos de la base
    #prospectos = Prospecto.objects.all()
    prostpecto_activo = Prospecto.objects.filter(Activo=True)
    context = {
        'prospectos':prostpecto_activo,
        'titulo': 'Prospectos',
        }
    # Desplegar la página de prospectos con enlistados con la información de la base de datos
    return render(request, 'prospectos/prospectos.html', context)


@login_required
@group_required('vendedora','administrador')
def lista_prospectos_inactivo(request):
    # Tomar los  los prospectos de la base
    # prospectos = Prospecto.objects.all()
    prostpecto_inactivo = Prospecto.objects.filter(Activo=False)
    context = {
        'prospectos':prostpecto_inactivo,
        'titulo': 'Prospectos inactivos',
        }
    # Desplegar la página de prospectos con enlistados con la información de la base de datos
    return render(request, 'prospectos/prospectos.html', context)


@login_required
@group_required('vendedora','administrador')
def baja_prospecto(request, id):
    prospecto = Prospecto.objects.get(id=id)
    if prospecto.Activo:
        prospecto.Activo = False
        prospecto.save()
        return redirect(reverse('prospectos:lista_prospectos'))
    else:
        prospecto.Activo = True
        prospecto.save()
        return redirect(reverse('prospectos:lista_prospectos_inactivo'))


@login_required
@group_required('vendedora', 'administrador')
def info_prospecto(request, id):
    prospecto = Prospecto.objects.get(id=id)
    # cursos = prospecto.Cursos.all()
    cursos = ProspectoEvento.objects.filter(Prospecto=prospecto)
    actividades = Actividad.objects.filter(prospecto_evento__Prospecto=prospecto).order_by('fecha').order_by('hora')
    titulo = 'Información de prospecto'
    agenda = []
    bitacora = []
    for actividad in actividades:
        if actividad.agenda():
            agenda.append(actividad)
        elif actividad.bitacora():
            bitacora.append(actividad)
    context = {
        'prospecto': prospecto,
        'titulo': titulo,
        'actividades': actividades,
        'agenda': agenda,
        'bitacora': bitacora,
        'cursos': cursos,
    }
    return render(request, 'prospectos/info_prospecto.html', context)

@login_required
@group_required('vendedora','administrador')
def lista_empresa(request):
    empresas = Empresa.objects.all()
    context = {
        'empresas':empresas,
        'titulo': 'Empresas',
        }
    return render(request, 'empresas/empresas.html', context)

@login_required
@group_required('vendedora','administrador')

#US14
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
            return lista_empresa(request)
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


#US
@login_required
@group_required('vendedora','administrador')
def lista_actividades(request,id):
    actividades = Actividad.objects.filter(prospecto_evento=id)
    context = {
        'actividades':actividades,
        'id':id
        }
    return render(request, 'actividades/actividades.html', context)


#US12
@login_required
@group_required('vendedora', 'administrador')
def crear_actividad(request, id):
    NewActividadForm = FormaActividad()
    # SI HAY UNA FORMA ENVIADA EN POST
    if request.method == 'POST':
        NewActividadForm = FormaActividad(request.POST)
        prospectoEvento = ProspectoEvento.objects.get(id=id)
        # SI LA FORMA ES VÁLIDA
        if NewActividadForm.is_valid():
            actividad = NewActividadForm.save(commit=False)
            # SE GUARDA LA NOTA
            actividad.prospecto_evento = prospectoEvento
            actividad.save()
            #Mensaje éxito
            messages.success(request, 'La actividad ha sido agregada')
            return lista_actividades(request,id)
        else:
            #Mensaje error
            messages.success(request, 'Forma inválida')
            context = {
                'form': NewActividadForm,
                'titulo': 'Agregar actividad',
                'id': id
            }
            return render(request, 'actividades/crear_actividad.html', context)
    # CARGAR LA VISTA
    context = {
        'form': NewActividadForm,
        'titulo': 'Agregar actividad',
        'id': id
    }
    return render(request, 'actividades/crear_actividad.html', context)


@login_required
@group_required('administrador')
def nuevo_pago(request, idPE):

    print(idPE)

    # recibir forma
    forma_pago = PagoForm()
    # si se recibe una forma con post
    if request.method == 'POST':
        print("entró")
        Forma_nuevo_pago = PagoForm(request.POST)
        # si la forma es válida
        if Forma_nuevo_pago.is_valid():

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
                print(idPE)
                print(pago.id)
                pe = ProspectoEvento.objects.get(id = idPE)
                return redirect('prospectos:lista_pagos', id=pe.Prospecto_id, idPE=idPE)
            else:
                return redirect('prospectos:crear_cliente', id=pago.id)

            # else:
            #     context = {
            #         'form': Forma_nuevo_pago,
            #         'titulo': 'Agregar Pago',
            #         'error_message':
            #     }
            #     return render(request, 'pagos/nuevo_pago.html', context)


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


        pe = ProspectoEvento.objects.get(id = idPE)
        curso = Curso.objects.get(id = pe.Curso_id)

        #VALIDAR QUE EL PAGO NO SUPERE EL MONTO MÁXIMO
        monto_maximo = curso.Costo - total_pagos


        # se renderea la página
        context = {
            'form': forma_pago,
            'titulo': 'Agregar Pago',
            'monto_maximo': monto_maximo,
        # 'eventos': Evento.objects.all().order_by('Nombre')
        }
        return render(request, 'pagos/nuevo_pago.html', context)


@login_required
@group_required('administrador')
def lista_pagos(request, id, idPE):

    # prospecto_evento = ProspectoEvento.objects.get(id = idPE)

    pagos = Pago.objects.filter(prospecto_evento_id = idPE).count()

    pe = ProspectoEvento.objects.get(id = idPE)

    # print(pe.Curso_id)

    total_pagos = 0

    pagos2 = Pago.objects.filter(prospecto_evento_id = idPE)

    for pago in pagos2:
        total_pagos += pago.monto

    curso = Curso.objects.get(id = pe.Curso_id)

    if(pagos > 0):
        context = {
            'titulo': 'Lista de Pagos',
            'prospecto': Prospecto.objects.get(id=id),
            'pagos': Pago.objects.filter(prospecto_evento_id = idPE).order_by('fecha'),
            'cliente': Cliente.objects.get(ProspectoEvento_id = idPE),
            'idPE': idPE,
            'curso': curso,
            'subtotal': total_pagos,
            'restante': curso.Costo - total_pagos,
        }
        return render(request, 'pagos/lista_pagos.html', context)
    else:

        return redirect('prospectos:nuevo_pago', idPE = idPE)
