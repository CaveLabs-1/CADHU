from .models import Curso
from django import forms

#ID US32 Forma
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = (
            'nombre',
            'descripcion',
        )
        exclude = {
            'activo',
        }
