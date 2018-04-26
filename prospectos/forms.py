from .models import Empresa, Prospecto, Lugar, ProspectoGrupo, Cliente, Pago
from grupos.models import Grupo
from django.forms import ModelForm
from django import forms
from . import models
from CADHU.settings import common


class EmpresaForm(ModelForm):
    class Meta:
        model = Empresa
        fields = (
            'nombre',
            'contacto_1',
            "contacto_2",
            'telefono_1',
            'telefono_2',
            'email_1',
            'email_2',
            'puesto_1',
            'puesto_2',
            'razon_social',
        )


class InscribirEmpresaForm(ModelForm):
    class Meta:
        model = Prospecto
        fields = (
            'empresa',
        )


class ProspectoForm(ModelForm):
    class Meta:
        model = Prospecto
        fields = (
            "nombre",
            'apellidos',
            'telefono_casa',
            'telefono_celular',
            'email',
            'metodo_captacion',
            'estado_civil',
            'ocupacion',
            'hijos',
            'recomendacion',
            'activo',
            'comentarios',
        )
        exclude = [
            'activo',
        ]


class LugarForm(ModelForm):
    class Meta:
        model = Lugar
        fields = (
            'calle',
            'numero_interior',
            'numero_exterior',
            'colonia',
            'ciudad',
            'estado',
            'pais',
            'codigo_postal',
        )


class FormaActividad(ModelForm):
    class Meta:
        model = models.Actividad
        fields = [
            'tipo',
            'titulo',
            'prospecto_grupo',
            'fecha',
            'hora',
            'notas',
            'terminado',
        ]
        exclude = [
            'prospecto_grupo'
        ]
        help_texts = {
            'fecha': 'Para agendar una actividad en un futuro, seleccione la fecha a realizarla.',
            'hora': 'Este campo es opcional.',
        }
        widgets = {
            'fecha': forms.DateInput(format=common.DATE_INPUT_FORMATS),
            'time': forms.TimeInput(),
            'notas': forms.Textarea(),
            'terminado': forms.CheckboxInput(),
            'tipo': forms.Select
        }


class ProspectoGrupoForm(ModelForm):
    class Meta:
        model = ProspectoGrupo
        fields = (
            'grupo',
            'interes',
            'flag_cadhu',
        )
        exclude = {
            'fecha',
            'prospecto',
            'user',
            'status',
        }

    def __init__(self, *args, **kwargs):
        super(ProspectoGrupoForm, self).__init__(*args, **kwargs)
        self.fields['grupo'].queryset = Grupo.objects.filter(activo=True)


class ProspectoGrupoEdit(ModelForm):
    class Meta:
        model = ProspectoGrupo
        fields = (
            'interes',
            'flag_cadhu',
        )


class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = (
            'matricula',
            'rfc',
            'direccion_facturacion',
            'razon_social',
        )
        excludes = {
            'prospecto_grupo',
            'fecha',
        }


class PagoForm(ModelForm):
    class Meta:
        model = Pago
        fields = (
            'fecha',
            'monto',
            'referencia',
            'comentarios',
            'tipo_pago',
        )
        excludes = (
            'prospecto_grupo',
        )
