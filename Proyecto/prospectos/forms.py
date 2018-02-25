from .models import Prospecto, Lugar
from django import forms

class ProspectoForm(forms.ModelForm):
    class Meta:
        model = Prospecto
        fields = (
            'Nombre',
            'Apellido_Paterno',
            'Apellido_Materno',
            'Telefono_Casa',
            'Telefono_Celular',
            'Email',
            'Metodo_Captacion',
            'Interes',
            'Estado_Civil',
            'Ocupacion',
            'Hijos',
        )

class LugarForm(forms.ModelForm):
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
