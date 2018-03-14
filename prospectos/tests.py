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
            'Telefono':'4422232226',
            'Email':'escuela@itesm.com',
            'Razon_Social':'Escuela'})
        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(resp.context['empresas'],['<Empresa: ITESM>'])

    #ACCEPTANCE CRITERIA: 13.3
    def test_ac_13_3(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'),{
            'Telefono':'4422232226',
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
            Telefono='4422232226',
            Email='correo@itesm.com',
            Direccion=Lugar.objects.get(Calle='Paraiso'),
            Razon_Social='Escuela'
        )
        resp = self.client.post(reverse('prospectos:crear_empresa'),{
            'Nombre':'ITESM',
            'Telefono':'4422232226',
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
                Apellidos='Martinez Villareal',
                Telefono_Casa='4422232226',
                Telefono_Celular='4422580662',
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
            Apellidos='Martinez Villareal',
            Telefono_Casa='4422232226',
            Telefono_Celular='4422580662',
            Email='pmartinez@gmail.com',
            Direccion=Lugar.objects.get(Calle='Paraiso'),
            Metodo_Captacion='Facebook',
            Estado_Civil='Soltero',
            Ocupacion='Estudiante',
            Hijos=1,
        )

    def test_ac_13_2(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'),{
            'Nombre':'ITESM',
            'Telefono':'4422232226',
            'Email':'escuela@itesm.com',
            'Razon_Social':'Escuela'})
        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(resp.context['empresas'],['<Empresa: ITESM>'])

    #ACCEPTANCE CRITERIA: 13.3
    def test_ac_13_3(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'),{
            'Telefono':'4422232226',
            'Email':'correo@itesm.com',
            'Razon_Social':'Escuela'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['Error'],'Forma invalida, favor de revisar sus respuestas de nuevo')

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
            Apellidos='Luna Calvillo',
            Telefono_Casa='4422232226',
            Telefono_Celular='4422580662',
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
                Apellidos='Luna Calvillo',
                Telefono_Casa='4422232226',
                Telefono_Celular='4422580662',
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
            Apellidos='Luna Calvillo',
            Telefono_Casa='4422232226',
            Telefono_Celular='4422580662',
            Email='a01209537@itesm.mx',
            Direccion=Lugar.objects.get(Calle='Lourdes'),
            Metodo_Captacion='Facebook',
            Estado_Civil='Soltero',
            Ocupacion='Estudiante',
            Hijos=1,
        )

        resp = self.client.post(reverse('prospectos:editar_prospecto', kwargs={'id': 1}),{
            'Nombre': 'Luis Alfredo', 'Apellidos': 'Rodriguez Santos',
            'Telefono_Casa': '4422232226', 'Telefono_Celular': '4422580662','Direccion':Lugar.objects.get(Calle='Lourdes'),
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
            Apellidos='Martinez Villareal',
            Telefono_Casa='4422232226',
            Telefono_Celular='4422580662',
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


class CargaMastivaTest(TestCase):
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
            Apellidos='Martinez Villareal',
            Telefono_Casa='4422232226',
            Telefono_Celular='4422580662',
            Email='mancha@cadhu.com',
            Direccion=lugar,
            Metodo_Captacion='Facebook',
            Estado_Civil='Soltero',
            Ocupacion='Estudiante',
            Hijos=1,
        )

        evento = Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')
        curso = Curso.objects.create(Nombre='CursoPrueba', Evento=evento, Fecha='2018-03-16', Direccion='Calle', Descripcion='Evento de marzo', Costo=1000)
        relacion = ProspectoEvento.objects.create(Prospecto = prospecto,Curso=curso,Interes='ALTO')
        csv = ['Nombre,Apellidos,Email,Telefono casa,Telefono celular,Metodo captacion,Estado civil,Ocupacion,Hijos,Recomendacion,Pais,Estado,Ciudad,Colonia,Calle,Numero exterior,Numero interior,Codigo postal,ID curso'
               ' \n Alejandro,Salmon FD,asalmon@cadhu.com,4423596210,,,,,0,,,,,,,,,,1 '
               '\n Marco,Luna Cal,marco@cadhu.com,,4423596210,,,,0,,,,,,,,,,1 '
               '\n Marqui,Mancha bla,mancha@cadhu.com,,,,,,0,,,,,,,,,,2 '
               '\n Alamito,tellez ajlssdf,alam@cadhu.com,,,,,,2,,,,,,,,,,1']
        with open('/test.csv', 'w') as f:
            f.write(csv)
            f.close()

        def test_ac_43_1(self):
            archivo = {'archivo': open('/test.csv', 'r')}
            resp = self.request.post(reverse('prospectos:carga_masiva'),{
                'archivo': archivo['archivo']
            })
            self.assertEqual(resp.context['archivo'], open('/test.csv', 'r'))



