from .models import Empresa, Prospecto, Lugar, ProspectoEvento, Cliente
from django.forms import ModelForm, inlineformset_factory
from django import forms
from . import models
from CADHU.settings import common

class EmpresaForm(ModelForm):
    class Meta:
        model = Empresa
        fields = (
            'Nombre',
            'Telefono',
            'Email',
            'Razon_Social',
        )


class ProspectoForm(ModelForm):
    class Meta:
        model = Prospecto
        fields = (
            'Nombre',
            'Apellidos',
            'Telefono_Casa',
            'Telefono_Celular',
            'Email',
            'Metodo_Captacion',
            'Estado_Civil',
            'Ocupacion',
            'Hijos',
            'Recomendacion',
        )


class LugarForm(ModelForm):
    class Meta:
        model = Lugar
        fields = (
            'Calle',
            'Numero_Interior',
            'Numero_Exterior',
            'Colonia',
            'Ciudad',
            'Estado',
            'Pais',
            'Codigo_Postal',
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
            'notas': forms.Textarea()
        }


class ProspectoEventoForm(ModelForm):
    class Meta:
        model = ProspectoEvento
        fields = (
            'Curso',
            'Interes',
            'FlagCADHU',
        )

        widgets = {
            'FlagCADHU': forms.CheckboxInput,
        }

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = (
            'Matricula',
        )
        excludes = {
            'ProspectoEvento',
            'Fecha',
        }
