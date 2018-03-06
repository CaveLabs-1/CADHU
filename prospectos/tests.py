from django.test import TestCase
from django.urls import reverse

from .models import Prospecto, Lugar
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
    @classmethod
    def setUpTestData(self):
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

    def test_nombre_label(self):
        prospecto = Prospecto.objects.get(Nombre='Pablo')
        field_label = prospecto._meta.get_field('Nombre').verbose_name
        self.assertEquals(field_label,'Nombre')

    def test_apellido_paterno_label(self):
        prospecto = Prospecto.objects.get(Nombre='Pablo')
        field_label = prospecto._meta.get_field('Apellido_Paterno').verbose_name
        self.assertEquals(field_label, 'Apellido Paterno')

    def test_apellido_materno_label(self):
        prospecto = Prospecto.objects.get(Nombre='Pablo')
        field_label = prospecto._meta.get_field('Apellido_Materno').verbose_name
        self.assertEquals(field_label, 'Apellido Materno')


    def test_telefono_casa_label(self):
        prospecto = Prospecto.objects.get(Nombre='Pablo')
        field_label = prospecto._meta.get_field('Telefono_Casa').verbose_name
        self.assertEquals(field_label, 'Telefono Casa')

    def test_telefono_celular_label(self):
        prospecto = Prospecto.objects.get(Nombre='Pablo')
        field_label = prospecto._meta.get_field('Telefono_Celular').verbose_name
        self.assertEquals(field_label, 'Telefono Celular')

    def test_email_label(self):
        prospecto = Prospecto.objects.get(Nombre='Pablo')
        field_label = prospecto._meta.get_field('Email').verbose_name
        self.assertEquals(field_label, 'Email')

    def test_metodo_captacion_label(self):
        prospecto = Prospecto.objects.get(Nombre='Pablo')
        field_label = prospecto._meta.get_field('Metodo_Captacion').verbose_name
        self.assertEquals(field_label, 'Metodo Captacion')

    def test_interes_label(self):
        prospecto = Prospecto.objects.get(Nombre='Pablo')
        field_label = prospecto._meta.get_field('Interes').verbose_name
        self.assertEquals(field_label, 'Interes')

    def test_estado_civil_label(self):
        prospecto = Prospecto.objects.get(Nombre='Pablo')
        field_label = prospecto._meta.get_field('Estado_Civil').verbose_name
        self.assertEquals(field_label, 'Estado Civil')

    def test_estado_civil_label(self):
        prospecto = Prospecto.objects.get(Nombre='Pablo')
        field_label = prospecto._meta.get_field('Estado_Civil').verbose_name
        self.assertEquals(field_label, 'Estado Civil')

    def test_ocupacion_label(self):
        prospecto = Prospecto.objects.get(Nombre='Pablo')
        field_label = prospecto._meta.get_field('Ocupacion').verbose_name
        self.assertEquals(field_label, 'Ocupacion')

    def test_hijos_label(self):
        prospecto = Prospecto.objects.get(Nombre='Pablo')
        field_label = prospecto._meta.get_field('Hijos').verbose_name
        self.assertEquals(field_label, 'Hijos')

    def test_recomendacion_label(self):
        prospecto = Prospecto.objects.get(Nombre='Pablo')
        field_label = prospecto._meta.get_field('Recomendacion').verbose_name
        self.assertEquals(field_label, 'Recomendacion')

    #Test Label Modelo Lugar
    def test_calle_label(self):
        lugar = Lugar.objects.get(Calle='Paraiso')
        field_label = lugar._meta.get_field('Calle').verbose_name
        self.assertEquals(field_label, 'Calle')

    def test_numero_exterior_label(self):
        lugar = Lugar.objects.get(Calle='Paraiso')
        field_label = lugar._meta.get_field('Numero_Exterior').verbose_name
        self.assertEquals(field_label, 'Numero Exterior')

    def test_numero_interior_label(self):
        lugar = Lugar.objects.get(Calle='Paraiso')
        field_label = lugar._meta.get_field('Numero_Interior').verbose_name
        self.assertEquals(field_label, 'Numero Interior')

    def test_colonia_label(self):
        lugar = Lugar.objects.get(Calle='Paraiso')
        field_label = lugar._meta.get_field('Colonia').verbose_name
        self.assertEquals(field_label, 'Colonia')

    def test_ciudad_label(self):
        lugar = Lugar.objects.get(Calle='Paraiso')
        field_label = lugar._meta.get_field('Ciudad').verbose_name
        self.assertEquals(field_label, 'Ciudad')

    def test_codigo_postal_label(self):
        lugar = Lugar.objects.get(Calle='Paraiso')
        field_label = lugar._meta.get_field('Codigo_Postal').verbose_name
        self.assertEquals(field_label, 'Codigo Postal')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/prospectos/crear')
        self.assertEqual(resp.status_code, 200)

    #Test Django
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


class ActividadTest(TestCase):
    @classmethod
    def setUpTestData(self):
        Actividad.objects.create(
            titulo='Test de  titulo',
            fecha='2018-02-02',
            hora='12:00',
            notas='Prueba de notas largas par al acreacion de un objeto que no es completamente necesario'
        )

    def test_view_url_exists_at_desired_location_and_uses_desired_template(self):
        resp = self.client.get('/prospectos/actividades')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'actividades/actividades.html')

    def test_createview_url_exists_at_desired_location_and_uses_desired_template(self):
        resp = self.client.get('/prospectos/actividades/crear')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'actividades/crear_actividad.html')

    def test_titulo_label(self):
        actividad = Actividad.objects.get(pk=1)
        field_label = actividad._meta.get_field('titulo').verbose_name
        self.assertEqual(field_label, 'Actividad')

    def test_fecha_label(self):
        actividad = Actividad.objects.get(pk=1)
        field_label = actividad._meta.get_field('fecha').verbose_name
        self.assertEqual(field_label, 'Fecha de la actividad')

    def test_hora_label(self):
        actividad = Actividad.objects.get(pk=1)
        field_label = actividad._meta.get_field('hora').verbose_name
        self.assertEqual(field_label, 'Hora de la actividad')

    def test_notas_label(self):
        actividad = Actividad.objects.get(pk=1)
        field_label = actividad._meta.get_field('hora').verbose_name
        self.assertEqual(field_label, 'Notas de la actividad')
