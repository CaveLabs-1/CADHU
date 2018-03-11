from django.test import TestCase, client
from django.urls import reverse
from .models import Empresa, Prospecto, Lugar
from .models import Prospecto, Lugar, ProspectoEvento
from eventos.models import Evento
from cursos.models import Curso
from django.db.models import QuerySet
from .models import Prospecto, Lugar, Actividad
from django.contrib.auth.models import User, Group
from django.urls import reverse
import string
import random
import datetime

class EmpresaTest(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
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

    #ACCEPTANCE CRITERIA: 13.2
    def test_ac_13_2(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'),{
            'Nombre':'ITESM',
            'Telefono':'+524422232226',
            'Email':'escuela@itesm.com',
            'Razon_Social':'Escuela'})
        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(resp.context['empresas'],['<Empresa: ITESM>'])

    #ACCEPTANCE CRITERIA: 13.3
    def test_ac_13_3(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'),{
            'Telefono':'+524422232226',
            'Email':'correo@itesm.com',
            'Razon_Social':'Escuela'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['Error'],'Forma invalida, favor de revisar sus respuestas de nuevo')

    #ACCEPTANCE CRITERIA: 13.4
    def test_ac_13_4(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'),{
            'Nombre':'ITESM',
            'Telefono':'ABC',
            'Email':'correo@itesm.com',
            'Razon_Social':'Escuela'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['Error'],'Forma invalida, favor de revisar sus respuestas de nuevo')

    #ACCEPTANCE CRITERIA: 13.6
    def test_ac_13_6(self):
        Empresa.objects.create(
            Nombre='ITESM',
            Telefono='+524422232226',
            Email='correo@itesm.com',
            Direccion=Lugar.objects.get(Calle='Paraiso'),
            Razon_Social='Escuela'
        )
        resp = self.client.post(reverse('prospectos:crear_empresa'),{
            'Nombre':'ITESM',
            'Telefono':'+524422232226',
            'Email':'correo@itesm.com',
            'Razon_Social':'Escuela'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['Error'],'Forma invalida, favor de revisar sus respuestas de nuevo')


class ProspectoListViewTest(TestCase):

    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

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
                Email=''.join([random.choice(string.ascii_letters + string.digits)for n in range(32)]) + '@gmail.com',
                Direccion=Lugar.objects.get(Calle='Paraiso'),
                Ocupacion='Estudiante',
            )

    #Acceptance citeria: 7.1
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/prospectos/')
        self.assertEqual(resp.status_code, 200)

    def test_view_prospectos_20(self):
        resp = self.client.get(reverse('prospectos:lista_prospectos'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['prospectos']),20)

class ProspectoTest(TestCase):

    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

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
            Estado_Civil='Soltero',
            Ocupacion='Estudiante',
            Hijos=1,
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
            Estado_Civil='Soltero',
            Ocupacion='Estudiante',
            Hijos=1,
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
                Estado_Civil='Soltero',
                Ocupacion='Estudiante',
                Hijos=1,
            )
            Prospecto_acum = Prospecto.objects.all().count()
            self.assertEqual(Prospecto_acum, 0)

        except:
            Prospecto_acum = Prospecto.objects.all().count()
            self.assertEqual(Prospecto_acum, 1)

    # ID_AC 4.1, 4.2
    def test_editar_prospecto(self):
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
            id='1',
            Nombre='Marco Antonio',
            Apellido_Paterno='Luna',
            Apellido_Materno='Calvillo',
            Telefono_Casa='+524422232226',
            Telefono_Celular='+524422580662',
            Email='a01209537@itesm.mx',
            Direccion=Lugar.objects.get(Calle='Lourdes'),
            Metodo_Captacion='Facebook',
            Estado_Civil='Soltero',
            Ocupacion='Estudiante',
            Hijos=1,
        )

        resp = self.client.post(reverse('prospectos:editar_prospecto', kwargs={'id': 1}),{
            'Nombre': 'Luis Alfredo', 'Apellido_Paterno': 'Rodriguez', 'Apellido_Materno': 'Santos',
            'Telefono_Casa': '+524422232226', 'Telefono_Celular': '+524422580662','Direccion':Lugar.objects.get(Calle='Lourdes'),
            'Email': 'a01209537@itesm.mx', 'Metodo_Captacion': 'Facebook',
            'Estado_Civil': 'SOLTERO', 'Ocupacion': 'Estudiante', 'Hijos': 1
        },follow=True)

        actualizado = Prospecto.objects.get(id=1)

        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(actualizado, 'Marco Antonio Luna Calvillo')

class ActividadTest(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')
        lugar = Lugar.objects.create(
            Calle='Paraiso',
            Numero_Interior='',
            Numero_Exterior='38',
            Colonia='Satelite',
            Estado='Queretaro',
            Ciudad='Queretaro',
            Pais='Mexico',
            Codigo_Postal='76125'

        )

        prospecto = Prospecto.objects.create(
            Nombre='Pablo',
            Apellido_Paterno='Martinez',
            Apellido_Materno='Villareal',
            Telefono_Casa='+524422232226',
            Telefono_Celular='+524422580662',
            Email='pmartinez@gmail.com',
            Direccion=lugar,
            Metodo_Captacion='Facebook',
            Estado_Civil='Soltero',
            Ocupacion='Estudiante',
            Hijos=1,
        )

        evento = Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')
        curso = Curso.objects.create(Nombre='CursoPrueba', Evento=evento, Fecha='2018-03-16', Direccion='Calle', Descripcion='Evento de marzo', Costo=1000)
        relacion = ProspectoEvento.objects.create(Prospecto = prospecto,Curso=curso,Interes='ALTO')

    #ACCEPTANCE CRITERIA: 12.1
    def test_ac_12_1(self):
        resp = self.client.post(reverse('prospectos:crear_actividad',kwargs={'id':1}),{
            'titulo':'Llamada con el prospecto',
            'fecha':datetime.datetime.now().date(),
            'notas':'Llamada con el prosecto',
            'prospecto_evento':1})
        self.assertQuerysetEqual(resp.context['actividades'],['<Actividad: Llamada con el prospecto>'])

    #ACCEPTANCE CRITERIA: 12.2
    def test_ac_12_2(self):
        resp = self.client.post(reverse('prospectos:crear_actividad',kwargs={'id':1}),{
            'titulo':'Llamada con el prospecto',
            'fecha':'2018-03-07',
            'hora':'Hora',
            'notas':'Llamada con el prosecto'})
        self.assertEqual(resp.context['titulo'],'Agregar actividad')
