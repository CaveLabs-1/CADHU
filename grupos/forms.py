from django import forms
from CADHU.settings import common
from .models import Grupo

from django.forms import widgets


class FormaGrupo(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = [
            'nombre',
            "curso",
            'fecha_inicio',
            'fecha_fin',
            'direccion',
            'descripcion',
            'costo',
            'encargado',
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(format='%Y-%m-%d'),
            'fecha_fin': forms.widgets.DateInput(format=common.DATE_INPUT_FORMATS),
        }
        input_formats = {
            'fecha_inicio': '%Y-%m-%d',
            'fecha_fin': '%Y-%m-%d',
        }
