from django import forms
from CADHU.settings import common
from .models import Curso

from django.forms import widgets



class FormaCurso(forms.ModelForm):

    class Meta:
        model = Curso
        fields = [
            'Nombre',
            'Evento',
            'Fecha_Inicio',
            'Fecha_Fin',
            'Direccion',
            'Descripcion',
            'Costo',
            'Encargado',
        ]
        widgets = {
            'Fecha_Inicio': forms.DateInput(format='%Y-%m-%d'),
            'Fecha_Fin': forms.widgets.DateInput(format=common.DATE_INPUT_FORMATS),
        }
        input_formats = {
            'Fecha_Inicio': '%Y-%m-%d',
            'Fecha_Fin': '%Y-%m-%d',
        }
