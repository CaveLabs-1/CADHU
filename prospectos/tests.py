from django.test import TestCase
from django.db.models import QuerySet
from .models import Prospecto, Lugar, Actividad
from django.urls import reverse
import string
import random

# Create your tests here.

class ProspectoListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_prospectos = 20
        N = 10

        Lugar.objects.create(
            Calle='Paraiso',
            Numero_Interior='',
            Numero_Exterior='38',
            Colonia='Satelite',
            Estado='Queretaro',
            Ciudad='Queretaro',
            Pais='Mexico',
            Codigo_Postal='76125'

        )

        for prospecto in range(number_of_prospectos):

            Prospecto.objects.create(
                Nombre='Pablo',
                Apellido_Paterno='Martinez',
                Apellido_Materno='Villareal',
                Telefono_Casa='+524422232226',
                Telefono_Celular='+524422580662',
                Email=''.join(random.choices(string.ascii_uppercase + string.digits, k=N)) + '@gmail.com',
                Direccion=Lugar.objects.get(Calle='Paraiso'),
                Metodo_Captacion='Facebook',
                Interes='Alto',
                Estado_Civil='Soltero',
                Ocupacion='Estudiante',
                Hijos=True,
            )

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/prospectos/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('prospectos:lista_prospectos'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('prospectos:lista_prospectos'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'prospectos/prospectos.html')



class ProspectoTest(TestCase):

    def setUp(self):
        Lugar.objects.create(
            Calle='Paraiso',
            Numero_Interior='',
            Numero_Exterior='38',
            Colonia='Satelite',
            Estado='Queretaro',
            Ciudad='Queretaro',
            Pais='Mexico',
            Codigo_Postal='76125'

        )

        Prospecto.objects.create(
            Nombre='Pablo',
            Apellido_Paterno='Martinez',
            Apellido_Materno='Villareal',
            Telefono_Casa='+524422232226',
            Telefono_Celular='+524422580662',
            Email='pmartinez@gmail.com',
            Direccion=Lugar.objects.get(Calle='Paraiso'),
            Metodo_Captacion='Facebook',
            Interes='Alto',
            Estado_Civil='Soltero',
            Ocupacion='Estudiante',
            Hijos=True,
        )

    def test_crear_prospecto(self):

        Lugar.objects.create(
            Calle='Lourdes',
            Numero_Interior='4',
            Numero_Exterior='105',
            Colonia='Satelite',
            Estado='Queretaro',
            Ciudad='Queretaro',
            Pais='Mexico',
            Codigo_Postal='76125'

        )

        Prospecto.objects.create(
            Nombre='Marco Antonio',
            Apellido_Paterno='Luna',
            Apellido_Materno='Calvillo',
            Telefono_Casa='+524422232226',
            Telefono_Celular='+524422580662',
            Email='a01209537@itesm.mx',
            Direccion=Lugar.objects.get(Calle='Lourdes'),
            Metodo_Captacion='Facebook',
            Interes='Alto',
            Estado_Civil='Soltero',
            Ocupacion='Estudiante',
            Hijos=True,
        )

        Prospecto_acum = Prospecto.objects.filter(Email='a01209537@itesm.mx').count()
        self.assertEqual(Prospecto_acum, 1)

    def test_prospecto_mismo_mail(self):

        try:

            Prospecto.objects.get_or_create(
                Nombre='Marco Antonio',
                Apellido_Paterno='Luna',
                Apellido_Materno='Calvillo',
                Telefono_Casa='+524422232226',
                Telefono_Celular='+524422580662',
                Email='pmartinez@gmail.com',
                Direccion=Lugar.objects.get(Calle='Paraiso'),
                Metodo_Captacion='Facebook',
                Interes='Alto',
                Estado_Civil='Soltero',
                Ocupacion='Estudiante',
                Hijos=True,
            )
            Prospecto_acum = Prospecto.objects.all().count()
            self.assertEqual(Prospecto_acum, 0)

        except:
            Prospecto_acum = Prospecto.objects.all().count()
            self.assertEqual(Prospecto_acum, 1)
