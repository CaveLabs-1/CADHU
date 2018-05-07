from django.shortcuts import render, redirect, reverse
from .models import Cliente, Empresa, Prospecto, Lugar, Actividad, ProspectoGrupo, Grupo, Pago
from grupos.models import Grupo
from tablib import Dataset
import datetime
from django.db.utils import IntegrityError
from .forms import FormaActividad, ClienteForm, EmpresaForm, ProspectoForm, LugarForm, ProspectoGrupoForm, \
    ProspectoGrupoEdit, PagoForm
from django.contrib.auth.decorators import login_required
from CADHU.decorators import group_required
from django.contrib import messages
from django.urls import reverse
from django.http import *
from django.utils.timezone import now

# --------------------------- PROSPECTO ------------------------------


# US43
@login_required
@group_required('vendedora', 'administrador')
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
                    calle=imported_data['Calle'][i],
                    numero_interior=imported_data['Numero interior'][i],
                    numero_exterior=imported_data['Numero exterior'][i],
                    colonia=imported_data['Colonia'][i],
                    ciudad=imported_data['Ciudad'][i],
                    estado=imported_data['Estado'][i],
                    pais=imported_data['Pais'][i],
                    codigo_postal=imported_data['Codigo postal'][i],
                )
                try:
                    # Busca en la base de datos por si existe este prospecto para solo crear la relacion
                    prospecto, created = Prospecto.objects.get_or_create(
                        nombre=imported_data['Nombre'][i],
                        apellidos=imported_data['Apellidos'][i],
                        email=imported_data['Email'][i],
                        telefono_casa=imported_data['Telefono casa'][i],
                        telefono_celular=imported_data['Telefono celular'][i],
                        metodo_captacion=imported_data['Metodo captacion'][i],
                        estado_civil=imported_data['Estado civil'][i],
                        ocupacion=imported_data['Ocupacion'][i],
                        hijos=int(imported_data['Hijos'][i]),
                        recomendacion=imported_data['Recomendacion'][i],
                        direccion=lugar,
                        activo=True,
                        empresa=None,
                        comentarios='Este prospecto fué creado a traves de carga masiva'
                    )
                    if created:
                        resultado[i] = 'El prospecto se creó con éxito '
                    else:
                        resultado[i] = 'El prospecto ya existía '
                    # obtiene el grupo
                    try:
                        grupo = Grupo.objects.get(id=imported_data['ID grupo'][i])
                        if grupo:
                            # crea la relacion
                            prospecto_grupo, created2 = ProspectoGrupo.objects.get_or_create(
                                prospecto=prospecto,
                                grupo=grupo,
                                fecha=datetime.datetime.now().date(),
                                interes='BAJO',
                                flag_cadhu=False,
                            )
                            if created2:
                                resultado[i] += ' y se relacionó con el grupo: ' + grupo.nombre
                            else:
                                resultado[i] += ' ya existía la relación con el grupo: ' + grupo.nombre
                    except Grupo.DoesNotExist:
                        resultado[i] += ' y no existe este grupo.'
                except IntegrityError:
                    resultado[i] = 'Hubo un error al subir este prospecto, revisar información y buscar ' \
                                   'repetidos en el sistema'
            except:
                resultado[i] = ''
        # escribe el resultado en ultima columna del excel
        dataset.append_col(resultado, header='Estado')
        with open('static/files/resultado.xls', 'wb') as f:
            f.write(dataset.export('xls'))
            f.close()
        messages.error(request, 'La carga masiva ha sido exitosa')
        return HttpResponseRedirect(reverse('prospectos:lista_prospectos'))


# US3
@login_required
@group_required('vendedora', 'administrador')
def crear_prospecto(request):
    new_prospecto_form = ProspectoForm(prefix='NewProspectoForm')
    new_lugar_form = LugarForm(prefix='NewLugarForm')
    # Si es petición POST, procesar la información de la forma
    if request.method == 'POST':
        # Crear la instancia de la forma y llenarla con los datos
        new_prospecto_form = ProspectoForm(request.POST, prefix='NewProspectoForm')
        new_lugar_form = LugarForm(request.POST, prefix='NewLugarForm')
        # Validar la forma y guardar en BD
        if new_prospecto_form.is_valid() and new_lugar_form.is_valid():
            print(new_lugar_form.is_valid())
            print(new_prospecto_form.is_valid())
            lugar = new_lugar_form.save()
            prospecto = new_prospecto_form.save(commit=False)
            prospecto.direccion = lugar
            prospecto.usuario = request.user
            prospecto.fecha_creacion = now()
            prospecto.save()
            messages.success(request, 'El prospecto ha sido creado exitosamente')
            return redirect('prospectos:info_prospecto', pk=prospecto.id)
        # Si la forma no es válida, volverla a mandar
        messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
        context = {
            'new_prospecto_form': new_prospecto_form,
            'new_lugar_form': new_lugar_form,
            'titulo': 'Registrar un Prospecto',
        }
        return render(request, 'prospectos/prospectos_form.html', context)
    # Si no es POST, volverla a mandar
    context = {
        'new_prospecto_form': new_prospecto_form,
        'new_lugar_form': new_lugar_form,
        'titulo': 'Registrar un Prospecto',
    }
    return render(request, 'prospectos/prospectos_form.html', context)


# US4
@login_required
@group_required('vendedora', 'administrador')
def editar_prospecto(request, pk):
    id_prospecto = Prospecto.objects.get(id=pk)
    new_prospecto_form = ProspectoForm(instance=id_prospecto)
    new_lugar_form = LugarForm(instance=id_prospecto.direccion)
    if request.method == 'POST':
        new_prospecto_form = ProspectoForm(request.POST or None, instance=id_prospecto)
        new_lugar_form = LugarForm(request.POST or None, instance=id_prospecto.direccion)
        if new_prospecto_form.is_valid() and new_lugar_form.is_valid():
            prospecto = new_prospecto_form.save(commit=False)
            lugar = new_lugar_form.save()
            prospecto.direccion = lugar
            prospecto.save()
            messages.success(request, 'El prospecto ha sido actualizado.')
            return redirect('prospectos:info_prospecto', pk=prospecto.id)
        else:
            messages.success(request, 'Existe una falla en los campos.')
            context = {
                'new_prospecto_form': new_prospecto_form,
                'new_lugar_form': new_lugar_form,
                'prospecto': id_prospecto,
                'titulo': 'Editar Prospecto',
            }
            return render(request, 'prospectos/prospectos_form.html', context)
    context = {
        'new_prospecto_form': new_prospecto_form,
        'new_lugar_form': new_lugar_form,
        'prospecto': id_prospecto,
        'titulo': 'Editar Prospecto',
    }
    return render(request, 'prospectos/prospectos_form.html', context)


# US7
@login_required
@group_required('vendedora', 'administrador')
def lista_prospectos(request):
    # Tomar los  los prospectos de la base
    # prospectos = Prospecto.objects.all()
    prospecto_activo = Prospecto.objects.filter(activo=True)
    context = {
        'prospectos': prospecto_activo,
        'titulo': 'Prospectos',
    }
    # Desplegar la página de prospectos con enlistados con la información de la base de datos
    return render(request, 'prospectos/prospectos.html', context)


# US6
@login_required
@group_required('vendedora', 'administrador')
def lista_prospectos_inactivo(request):
    # Tomar los  los prospectos de la base
    # prospectos = Prospecto.objects.all()
    prostpecto_inactivo = Prospecto.objects.filter(activo=False)
    context = {
        'prospectos': prostpecto_inactivo,
        'titulo': 'Prospectos inactivos',
    }
    # Desplegar la página de prospectos con enlistados con la información de la base de datos
    return render(request, 'prospectos/prospectos.html', context)


# US6
@login_required
@group_required('vendedora', 'administrador')
def baja_prospecto(request, pk):
    # Obtener el prospecto
    prospecto = Prospecto.objects.get(id=pk)
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
def info_prospecto(request, pk):
    new_prospecto_grupo_form = ProspectoGrupoForm()
    prospecto = Prospecto.objects.get(id=pk)
    grupos = ProspectoGrupo.objects.filter(prospecto=prospecto)
    actividades = Actividad.objects.filter(prospecto_grupo__prospecto=prospecto).order_by('fecha', 'hora')
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
        new_prospecto_grupo_form = ProspectoGrupoForm(request.POST)
        # Validar la forma
        if new_prospecto_grupo_form.is_valid():
            prospecto_grupo = new_prospecto_grupo_form.save(commit=False)
            # Validar que no se este agregando un grupo repetido
            try:
                ProspectoGrupo.objects.get(prospecto=prospecto, grupo=prospecto_grupo.grupo)
                messages.success(request, 'El grupo que quiere asignar ya ha sido asignado')
                context = {
                    'prospecto': prospecto,
                    'new_prospecto_grupo_form': new_prospecto_grupo_form,
                    'titulo': titulo,
                    'actividades': actividades,
                    'agenda': agenda,
                    'bitacora': bitacora,
                    'grupos': grupos,
                }
                return render(request, 'prospectos/info_prospecto.html', context)
            # Guardar la forma en la BD
            except ProspectoGrupo.DoesNotExist:
                prospecto_grupo.prospecto = prospecto
                prospecto_grupo.flag_cadhu = False
                prospecto_grupo.fecha = now()
                prospecto_grupo.save()
                messages.success(request, 'Grupo asignado a prospecto')
                context = {
                    'prospecto': prospecto,
                    'new_prospecto_grupo_form': new_prospecto_grupo_form,
                    'actividades': actividades,
                    'agenda': agenda,
                    'bitacora': bitacora,
                    'titulo': titulo,
                    'grupos': grupos
                }
                return render(request, 'prospectos/info_prospecto.html', context)
        messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
    context = {
        'prospecto': prospecto,
        'new_prospecto_grupo_form': new_prospecto_grupo_form,
        'actividades': actividades,
        'agenda': agenda,
        'titulo': titulo,
        'bitacora': bitacora,
        'grupos': grupos,
    }
    return render(request, 'prospectos/info_prospecto.html', context)


# ---------------------------------- PROSPECTO GRUPO ----------------------------------


# US26
@login_required
@group_required('vendedora', 'administrador')
def registrar_grupos(request, pk):
    new_prospecto_grupo_form = ProspectoGrupoForm()
    prospecto = Prospecto.objects.get(id=pk)
    grupos = ProspectoGrupo.objects.filter(prospecto=prospecto)
    # Si es petición POST, procesar la información de la forma
    if request.method == 'POST':
        # Crear la instancia de la forma y llenarla con los datos
        new_prospecto_grupo_form = ProspectoGrupoForm(request.POST)
        if new_prospecto_grupo_form.grupo.activo:
            # Validar la forma
            if new_prospecto_grupo_form.is_valid():
                prospecto_grupo = new_prospecto_grupo_form.save(commit=False)
                # Validar que no se este agregando un grupo repetido
                try:
                    ProspectoGrupo.objects.get(prospecto=prospecto, grupo=prospecto_grupo.grupo)
                    messages.success(request, 'El grupo que quiere asignar ya ha sido asignado')
                    context = {
                        'prospecto': prospecto,
                        'new_prospecto_grupo_form': new_prospecto_grupo_form,
                        'titulo': 'Registrar Registrar Grupos - ' + prospecto.nombre + ' ' + prospecto.apellidos,
                        'grupos': grupos,
                    }
                    return render(request, 'grupos/prospecto_grupo_form.html', context)
                # Guardar la forma en la BD
                except ProspectoGrupo.DoesNotExist:
                    prospecto_grupo.prospecto = prospecto
                    prospecto_grupo.flag_cadhu = False
                    prospecto_grupo.fecha = now()
                    prospecto_grupo.save()
                    messages.success(request, 'Grupo asignado a prospecto')
                    context = {
                        'prospecto': prospecto,
                        'new_prospecto_grupo_form': new_prospecto_grupo_form,
                        'titulo': 'Registrar Grupos - ' + prospecto.nombre + ' ' + prospecto.apellidos,
                        'grupos': grupos,
                    }
                    return render(request, 'grupos/prospecto_grupo_form.html', context)
            messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
        messages.success(request, 'No se puede inscribir a un grupo inactivo.')
    context = {
        'prospecto': prospecto,
        'new_prospecto_grupo_form': new_prospecto_grupo_form,
        'titulo': 'Registrar Grupos - ' + prospecto.nombre + ' ' + prospecto.apellidos,
        'grupos': grupos,
    }
    return render(request, 'grupos/prospecto_grupo_form.html', context)


# US11
@login_required
@group_required('vendedora', 'administrador')
def editar_grupo(request, pk):
    old_prospecto_grupo_form = ProspectoGrupoForm()
    grupo_editar = ProspectoGrupo.objects.get(id=pk)
    new_prospecto_grupo_form = ProspectoGrupoEdit(instance=grupo_editar)
    prospecto = grupo_editar.prospecto
    grupos = ProspectoGrupo.objects.filter(prospecto=prospecto)
    # Si es petición POST, procesar la información de la forma
    if request.method == 'POST':
        # Crear la instancia de la forma y llenarla con los datos
        new_prospecto_grupo_form = ProspectoGrupoEdit(request.POST or None, instance=grupo_editar)
        # Validar la forma y guardarla en la BD
        if new_prospecto_grupo_form.is_valid():
            prospecto_grupo = new_prospecto_grupo_form.save(commit=False)
            prospecto_grupo.prospecto = prospecto
            prospecto_grupo.grupo = grupo_editar.grupo
            prospecto_grupo.save()
            messages.success(request, 'Grupo Modificado a prospecto')
            context = {
                'prospecto': prospecto,
                'new_prospecto_grupo_form': old_prospecto_grupo_form,
                'titulo': 'Registrar Grupos - ' + prospecto.nombre + ' ' + prospecto.apellidos,
                'grupos': grupos,
            }
            return redirect('prospectos:info_prospecto_grupo', pk)
        messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
    context = {
        'prospecto': prospecto,
        'new_prospecto_grupo_form': new_prospecto_grupo_form,
        'titulo': 'Editar Grupo - ' + grupo_editar.grupo.nombre,
        'grupos': grupos,
    }
    return render(request, 'grupos/prospecto_grupo_edit.html', context)


# US10
@login_required
@group_required('vendedora', 'administrador')
def eliminar_grupo(request, pk):
    grupo = ProspectoGrupo.objects.get(id=pk)
    new_prospecto_grupo_form = ProspectoGrupoForm()
    prospecto = grupo.prospecto
    grupos = ProspectoGrupo.objects.filter(prospecto=prospecto)
    if Pago.objects.filter(prospecto_grupo=grupo).count() > 0:
        messages.success(request, 'El prospecto ya ha realizado un pago, por ende, el grupo no puede ser eliminado')
        context = {
            'prospecto': prospecto,
            'new_prospecto_grupo_form': new_prospecto_grupo_form,
            'titulo': 'Registrar Grupo - ' + prospecto.nombre + ' ' + prospecto.apellidos,
            'grupos': grupos,
        }
        return render(request, 'grupos/prospecto_grupo_form.html', context)
    else:
        grupo.delete()
        messages.success(request, 'Grupo eliminado de manera exitosa')
        context = {
            'prospecto': prospecto,
            'new_prospecto_grupo_form': new_prospecto_grupo_form,
            'titulo': 'Registrar Grupo - ' + prospecto.nombre + ' ' + prospecto.apellidos,
            'grupos': grupos,
        }
        return render(request, 'grupos/prospecto_grupo_form.html', context)


# US23
@login_required
@group_required('vendedora', 'administrador')
def info_prospecto_grupo(request, rel):
    relacion = ProspectoGrupo.objects.get(id=rel)
    prospecto = Prospecto.objects.get(id=relacion.prospecto.id)
    titulo = 'Relación con: ' + str(relacion.grupo)
    context = {
        'relacion': relacion,
        'actividades': relacion.actividad_set.all(),
        'prospecto': prospecto,
        'titulo': titulo,
    }
    return render(request, 'grupos/info_prospecto_grupo.html', context)


# ------------------------------------ EMPRESAS ----------------------------------------

# US17
@login_required
@group_required('vendedora', 'administrador')
def lista_empresas(request):
    # Si las empresas son activas, desplegarlas
    empresas = Empresa.objects.filter(activo=True)
    context = {
        'empresas': empresas,
        'titulo': 'Empresas',
        'estatus': 'activo',
    }
    return render(request, 'empresas/empresas.html', context)


@login_required
@group_required('vendedora', 'administrador')
def lista_empresas_inactivo(request):
    # Tomar los  los empresas de la base inactivos
    empresa_inactivo = Empresa.objects.filter(activo=False)
    context = {
        'empresas': empresa_inactivo,
        'titulo': 'Empresas inactivas',
        'estatus': 'inactivo',
    }
    # Desplegar la página de empresas con enlistados con la información de la base de datos
    return render(request, 'empresas/empresas.html', context)


# US14
@login_required
@group_required('vendedora', 'administrador')
def editar_empresa(request, pk):
    # Obtener el id de la empresa, hacer nueva forma de la empresa y de lugar
    id_empresa = Empresa.objects.get(id=pk)
    new_empresa_form = EmpresaForm(instance=id_empresa)
    new_lugar_form = LugarForm(instance=id_empresa.direccion)
    if request.method == 'POST':
        new_empresa_form = EmpresaForm(request.POST or None, instance=id_empresa)
        new_lugar_form = LugarForm(request.POST or None, instance=id_empresa.direccion)
        # Si es válida, instanciar nueva empresa Y guardarla
        if new_empresa_form.is_valid() and new_lugar_form.is_valid():
            empresa = new_empresa_form.save(commit=False)
            lugar = new_lugar_form.save()
            empresa.direccion = lugar
            empresa.save()
            messages.success(request, 'La empresa ha sido actualizada.')
            return redirect('prospectos:lista_empresas')
        else:
            # Si no es válida, notificar al usuario
            messages.success(request, 'Existe una falla en los campos.')
            context = {
                'new_empresa_form': new_empresa_form,
                'new_lugar_form': new_lugar_form,
                'empresa': id_empresa,
                'titulo': 'Editar Empresa',
            }
            return render(request, 'empresas/empresas_form.html', context)
    context = {
        'new_empresa_form': new_empresa_form,
        'new_lugar_form': new_lugar_form,
        'empresa': id_empresa,
        'titulo': 'Editar Empresa',
    }
    return render(request, 'empresas/empresas_form.html', context)


# US13
@login_required
@group_required('vendedora', 'administrador')
def crear_empresa(request):
    new_empresa_form = EmpresaForm()
    new_lugar_form = LugarForm()
    # Si el método HTTP es post procesar la información de la forma:
    if request.method == "POST":
        # Definir el error para forma invalida:
        error = 'Forma invalida, favor de revisar sus respuestas de nuevo'
        # Crear y llenar la forma
        new_empresa_form = EmpresaForm(request.POST)
        new_lugar_form = LugarForm(request.POST)
        # Si la forma es válida guardar la información en la base de datos:
        if new_empresa_form.is_valid() and new_lugar_form.is_valid():
            lugar = new_lugar_form.save()
            empresa = new_empresa_form.save(commit=False)
            empresa.direccion = lugar
            empresa.save()
            return redirect('prospectos:lista_empresas')
        # Si la forma es inválida mostrar el error y volver a crear la form para llenarla de nuevo
        messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
        context = {
            'Error': error,
            'new_empresa_form': new_empresa_form,
            'new_lugar_form': new_lugar_form,
            'titulo': 'Registrar una Empresa',
        }
        return render(request, 'empresas/empresas_form.html', context)
    # Si el método HTTP no es post, volver a enviar la forma:
    context = {
        'new_empresa_form': new_empresa_form,
        'new_lugar_form': new_lugar_form,
        'titulo': 'Registrar una Empresa',
    }
    return render(request, 'empresas/empresas_form.html', context)


@login_required
@group_required('vendedora', 'administrador')
def empresa_info(request, pk):
    empresa = Empresa.objects.get(id=pk)
    prospectos = Prospecto.objects.filter(empresa=empresa)
    lugar = Lugar.objects.get(id=empresa.direccion.id)
    context = {
        'empresa': empresa,
        'prospectos': prospectos,
        'lugar': lugar,
        'titulo': empresa.nombre,
    }
    return render(request, 'empresas/empresas_info.html', context)


# US16 y US18
@login_required
@group_required('vendedora', 'administrador')
def baja_empresas(request, pk):
    # Obtener empresa
    empresa = Empresa.objects.get(id=pk)
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
@group_required('vendedora', 'administrador')
def inscribir_empresa(request, pk):
    empresa = Empresa.objects.get(id=pk)
    prospectos = Prospecto.objects.exclude(empresa__isnull=False) | Prospecto.objects.filter(empresa=empresa)
    if request.method == "POST":
        vaciar = Prospecto.objects.filter(empresa=empresa)
        for va in vaciar:
            va.empresa = None
            va.save()
        for algo in request.POST.getlist('prospectos[]'):
            prospect = Prospecto.objects.get(id=algo)
            prospect.empresa = empresa
            prospect.save()
        return empresa_info(request, pk)
    context = {
        'prospectos': prospectos,
        'empresa': empresa,
        'titulo': 'Asignar prospectos a: '+empresa.nombre,
    }
    return render(request, 'empresas/empresa_prospectos_form.html', context)


# ------------------------------------------- ACTIVIDADES ---------------------------------


# US15
@login_required
@group_required('vendedora', 'administrador')
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
            return redirect('prospectos:info_prospecto_grupo', pk)
        else:
            # Mensaje error
            error = 'Forma inválida'
            messages.success(request, 'Forma inválida')
            context = {
                'Error': error,
                'form': new_actividad_form,
                'titulo': 'Registrar actividad',
                'id': pk
            }
            return render(request, 'actividades/form_actividad.html', context)
    # CARGAR LA VISTA
    context = {
        'form': new_actividad_form,
        'titulo': 'Agregar actividad',
        'id': pk
    }
    return render(request, 'actividades/form_actividad.html', context)


# US12
@login_required
@group_required('vendedora', 'administrador')
def estado_actividad(request, pk):
    act = Actividad.objects.get(id=pk)
    if act.terminado:
        act.terminado = False
        act.save()
    else:
        act.terminado = True
        act.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# US12
@login_required
@group_required('vendedora', 'administrador')
def estado_flag(request, pk):
    rel = ProspectoGrupo.objects.get(id=pk)
    if rel.flag_cadhu:
        rel.flag_cadhu = False
        rel.save()
    else:
        rel.flag_cadhu = True
        rel.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# --------------------------------- PAGOS ------------------------------


# US41
@login_required
@group_required('administrador', 'vendedora')
def nuevo_pago(request, id_pe):
    # recibir forma
    forma_pago = PagoForm()
    # si se recibe una forma con post
    if request.method == 'POST':
        forma_nuevo_pago = PagoForm(request.POST)
        # si la forma es válida
        if forma_nuevo_pago.is_valid():
            # VALIDAR QUE EL PAGO NO SUPERE EL MONTO MÁXIMO
            # se guarda la forma
            pago = forma_nuevo_pago.save(commit=False)
            pago.prospecto_grupo_id = id_pe
            pago = forma_nuevo_pago.save()
            # se redirige a la próxima vista
            messages.success(request, 'Pago agregado exitosamente!')
            pagos = Pago.objects.filter(prospecto_grupo_id=id_pe).count()
            pe = ProspectoGrupo.objects.get(id=id_pe)
            if pe.cliente_set.exists():
                return redirect('prospectos:lista_pagos', id_pe=id_pe)
            else:
                return redirect('prospectos:crear_cliente', pk=pago.id)
        else:
            # se renderiza la forma nuevamente con los errores marcados
            context = {
                'form': forma_nuevo_pago,
                'titulo': 'Agregar Pago',
                'error_message': forma_nuevo_pago.errors
            }
            return render(request, 'pagos/nuevo_pago.html', context)
    else:
        total_pagos = 0
        query_pagos = Pago.objects.filter(prospecto_grupo_id=id_pe)
        for pago in query_pagos:
            total_pagos += pago.monto
        pe = ProspectoGrupo.objects.get(id=id_pe)
        grupo = Grupo.objects.get(id=pe.grupo_id)
        # VALIDAR QUE EL PAGO NO SUPERE EL MONTO MÁXIMO
        monto_maximo = grupo.costo - total_pagos
        # se renderiza la página
        context = {
            'form': forma_pago,
            'titulo': 'Registrar Pago',
            'monto_maximo': monto_maximo,
        }
        return render(request, 'pagos/nuevo_pago.html', context)


# US42
@login_required
@group_required('administrador', 'vendedora')
def lista_pagos(request, id_pe):
    pagos = Pago.objects.filter(prospecto_grupo_id=id_pe).count()
    pe = ProspectoGrupo.objects.get(id=id_pe)
    total_pagos = 0
    pagos2 = Pago.objects.filter(prospecto_grupo_id=id_pe)
    for pago in pagos2:
        total_pagos += pago.monto
    grupo = Grupo.objects.get(id=pe.grupo_id)
    if pagos > 0:
        context = {
            'titulo': 'Lista de Pagos',
            'prospecto': Prospecto.objects.get(id=pe.prospecto.id),
            'pagos': Pago.objects.filter(prospecto_grupo=pe).order_by('fecha'),
            'cliente': pe,
            'id_pe': id_pe,
            'grupo': grupo,
            'subtotal': total_pagos,
            'restante': grupo.costo - total_pagos,
            'costo': grupo.costo,
        }
        return render(request, 'pagos/lista_pagos.html', context)
    else:
        return redirect('prospectos:nuevo_pago', id_pe=id_pe)


# US42
@login_required
@group_required('administrador')
def autorizar_pago(request, pk):
    pago = Pago.objects.get(id=pk)
    if not pago.validado:
        pago.validado = True
        pago.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# ---------------------------- CLIENTES -------------------------------


# US38
@login_required
@group_required('vendedora', 'administrador')
def lista_clientes(request):
    # Tomar los  los clientes de la base de datos
    clientes = Cliente.objects.filter(activo=True)
    context = {
        'clientes': clientes,
        'titulo': 'Clientes',
        'estatus': 'activo',
    }
    # Desplegar la página de clientes con enlistados con la información de la base de datos
    return render(request, 'clientes/clientes.html', context)


# US39
@login_required
@group_required('vendedora', 'administrador')
def lista_clientes_inactivos(request):
    # Tomar los  los clientes inactivos de la base
    cliente_inactivo = Cliente.objects.filter(activo=False).order_by('fecha')
    context = {
        'cliente': cliente_inactivo,
        'titulo': 'Clientes',
    }
    # Desplegar la página de cliente con enlistados con la información de la base de datos
    return render(request, 'clientes/clientes.html', context)


# US30
@login_required
@group_required('vendedora', 'administrador')
def eliminar_cliente(request, pk):
    # Seleccionar el cliente y sus pagos de la base de datos
    cliente = Cliente.objects.get(id=pk)
    pagos = Pago.objects.filter(prospecto_grupo=cliente.prospecto_grupo)
    # Eliminar el cliente selecciondo
    cliente.delete()
    # Eliminar los pagos del cliente
    for pago in pagos:
        pago.delete()
    clientes = Cliente.objects.filter(activo=True).order_by('fecha')
    context = {
        'clientes': clientes,
        'titulo': 'Clientes',
        'estatus': 'activo',
    }
    # Desplegar la lista de clientes actualizada
    return render(request, 'clientes/clientes.html', context)


# US31
@login_required
@group_required('vendedora', 'administrador')
def crear_cliente(request, pk):
    new_cliente_form = ClienteForm()
    new_lugar_form = LugarForm()
    pago = Pago.objects.get(id=pk)
    # Si el método HTTP es post procesar la información de la forma:
    if request.method == "POST":
        # Crear y llenar la forma
        error = 'Forma invalida, favor de revisar sus respuestas de nuevo'
        new_cliente_form = ClienteForm(request.POST)
        new_lugar_form = LugarForm(request.POST)
        fecha = pago.fecha
        prospecto_grupo = ProspectoGrupo.objects.get(pk=pago.prospecto_grupo_id)
        # Si la forma es válida guardar la información en la base de datos:
        if new_cliente_form.is_valid():
            lugar = new_lugar_form.save()
            cliente = new_cliente_form.save(commit=False)
            cliente.prospecto_grupo = prospecto_grupo
            cliente.fecha = fecha
            cliente.direccion_facturacion = lugar
            prospecto_grupo.status = 'CURSANDO'
            prospecto_grupo.save()
            cliente.save()
            clientes = Cliente.objects.all()
            prospecto_grupo = ProspectoGrupo.objects.get(id=pago.prospecto_grupo_id)
            return redirect('prospectos:lista_pagos', id_pe=prospecto_grupo.id)
        # Si la forma es inválida mostrar el error y volver a crear la form para llenarla de nuevo
        messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
        context = {
            'Error': error,
            'new_cliente_form': new_cliente_form,
            'new_lugar_form': new_lugar_form,
            'titulo': 'Registrar un Cliente',
            'id_pe': pago.prospecto_grupo.id,
        }
        return render(request, 'clientes/crear_cliente.html', context)
    # Si el método HTTP no es post, volver a enviar la forma:
    context = {
        'new_cliente_form': new_cliente_form,
        'new_lugar_form': new_lugar_form,
        'titulo': 'Registrar Cliente',
        'id_pe': pago.prospecto_grupo.id,
    }
    return render(request, 'clientes/crear_cliente.html', context)


# US37
@login_required
@group_required('vendedora', 'administrador')
def editar_cliente(request, pk):
    prospecto_grupo = ProspectoGrupo.objects.get(id=pk)
    id_cliente = Cliente.objects.get(prospecto_grupo=prospecto_grupo)
    new_cliente_form = ClienteForm(instance=id_cliente)
    new_lugar_form = LugarForm(instance=id_cliente.direccion_facturacion)
    prospecto = Prospecto.objects.get(id=prospecto_grupo.prospecto_id)
    # Si el método HTTP es post procesar la información de la forma:
    if request.method == "POST":
        # Crear y llenar la forma
        error = 'Forma invalida, favor de revisar sus respuestas de nuevo'
        new_cliente_form = ClienteForm(request.POST or None, instance=id_cliente)
        new_lugar_form = LugarForm(request.POST or None, instance=id_cliente.direccion_facturacion)
        pago = Pago.objects.filter(prospecto_grupo=prospecto_grupo).order_by('fecha')
        fecha = pago[0].fecha
        # Si la forma es válida guardar la información en la base de datos:
        if new_cliente_form.is_valid():
            lugar = new_lugar_form.save()
            cliente = new_cliente_form.save(commit=False)
            cliente.prospecto_grupo = prospecto_grupo
            cliente.fecha = fecha
            cliente.direccion_facturacion = lugar
            prospecto_grupo.status = 'CURSANDO'
            prospecto_grupo.save()
            cliente.save()
            clientes = Cliente.objects.all()
            return redirect('prospectos:lista_pagos', id_pe=prospecto_grupo.id)
        # Si la forma es inválida mostrar el error y volver a crear la form para llenarla de nuevo
        messages.success(request, 'Forma invalida, favor de revisar sus respuestas de nuevo')
        context = {
            'Error': error,
            'new_cliente_form': new_cliente_form,
            'new_lugar_form': new_lugar_form,
            'titulo': 'Editar Cliente: ' + prospecto.nombre + " " + prospecto.apellidos,
            'id_pe': pk,
        }
        return render(request, 'clientes/crear_cliente.html', context)
    # Si el método HTTP no es post, volver a enviar la forma:
    context = {
        'new_cliente_form': new_cliente_form,
        'new_lugar_form': new_lugar_form,
        'titulo': 'Editar Cliente: ' + prospecto.nombre + " " + prospecto.apellidos,
        'id_pe': pk,
    }
    return render(request, 'clientes/crear_cliente.html', context)


# US39
@login_required
@group_required('administrador')
def baja_cliente(request, pk):
    cliente = Cliente.objects.get(id=pk)
    if cliente.activo:
        cliente.activo = False
        cliente.save()
        return redirect(reverse('prospectos:lista_prospectos'))
    else:
        cliente.activo = True
        cliente.save()
        return redirect(reverse('prospectos:lista_prospectos_inactivos'))


# US38
@login_required
@group_required('vendedora', 'administrador')
def info_cliente(request, pk):
    cliente = Cliente.objects.get(id=pk)
    lugar = Lugar.objects.get(id=cliente.direccion_facturacion.id)
    relacion = ProspectoGrupo.objects.get(id=cliente.prospecto_grupo.id)
    prospecto = Prospecto.objects.get(id=relacion.prospecto.id)
    context = {
        'cliente': cliente,
        'lugar': lugar,
        'relacion': relacion,
        'prospecto': prospecto,
        'titulo': 'Cliente:' + prospecto.nombre + " " + prospecto.apellidos,
    }
    return render(request, 'clientes/info_cliente.html', context)
