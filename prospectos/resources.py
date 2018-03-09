from import_export import resources
from .models import Prospecto, Lugar


class ProspectoResource(resources.ModelResource):
    class Meta:
        model = Prospecto
        exculde = ['Direccion', 'Metodo_Captacion', 'Interes', 'Estado_Civil']


class LugarResource(resources.ModelResource):
    class Meta:
        model = Lugar
