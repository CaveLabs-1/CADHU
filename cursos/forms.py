from django import forms

from .models import Curso

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
            'Fecha': forms.DateInput(),

        }
