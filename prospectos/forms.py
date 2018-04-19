from .models import Empresa, Prospecto, Lugar, ProspectoEvento, Cliente, Pago
from django.forms import ModelForm
from django import forms
from . import models
from CADHU.settings import common


class EmpresaForm(ModelForm):
    class Meta:
        model = Empresa
        fields = (
            'nombre',
            'Contacto1',
            'Contacto2',
            'Telefono1',
            'Telefono2',
            'Email1',
            'Email2',
            'Puesto1',
            'Puesto2',
            'Razon_Social',
        )

class Inscribir_EmpresaForm(ModelForm):
    class Meta:
        model = Prospecto
        fields = (
            'Empresa',
        )

class Prospecto_form(ModelForm):
    class Meta:
        model = Prospecto
        fields = (
            'nombre',
            'apellidos',
            'telefono_casa',
            'telefono_celular',
            'email',
            'metodo_captacion',
            'estado_civil',
            'ocupacion',
            'hijos',
            'recomendacion',
            'comentarios',
        )
        exclude = [
            'activo',
        ]


class Lugar_form(ModelForm):
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
            'codigo_Postal',
        )


class FormaActividad(ModelForm):
    class Meta:
        model = models.Actividad
        fields = [
            'titulo',
            'prospecto_evento',
            'fecha',
            'hora',
            'notas',
            'terminado',
        ]
        exclude = [
            'prospecto_evento'
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
        }


class ProspectoEventoForm(ModelForm):
    class Meta:
        model = ProspectoEvento
        fields = (
            'Curso',
            'Interes',
            'FlagCADHU',
        )


class ProspectoEventoEdit(ModelForm):
    class Meta:
        model = ProspectoEvento
        fields = (
            'Interes',
            'FlagCADHU',
        )



class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = (
            'matricula',
            'rfc',
            'direccionFacturacion',
            'razonSocial',
        )
        excludes = {
            'ProspectoEvento',
            'Fecha',
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
            'prospecto_evento',
        )
