from django.test import TestCase, client
from django.urls import reverse
from eventos.models import Evento
from cursos.models import Curso
from django.db.models import QuerySet
from .models import Prospecto, Lugar, Actividad, Empresa, ProspectoEvento, Cliente, Pago
from django.contrib.auth.models import User, Group
from django.urls import reverse
import string
import random
import datetime
import os

class ClienteTest(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        prospecto = Prospecto.objects.create(Nombre='Pablo', Apellidos='Martinez Villareal', Email='pmartinez@gmail.com')
        evento = Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')
        curso = Curso.objects.create(Nombre='CursoPrueba', Evento=evento, Direccion='Calle', Costo=1000)
        relacion = ProspectoEvento.objects.create(Prospecto=prospecto,Curso=curso,Interes='ALTO',FlagCADHU=False)
        pago = Pago.objects.create(monto=500, prospecto_evento=relacion)

    #ACCEPTANCE CRITERIA: 31.1
    def test_crear_cliente(self):
        resp = self.client.post(reverse('prospectos:crear_cliente', kwargs={'id':1}),{
             'Matricula':'A01206199'})
        self.assertEqual(resp.status_code, 302)
        Cliente_acum = Cliente.objects.filter(Matricula='A01206199').count()
        self.assertEqual(Cliente_acum, 1)

    #ACCEPTANCE CRITERIA: 31.1
    def test_editar_cliente(self):
        resp = self.client.post(reverse('prospectos:crear_cliente', kwargs={'id':1}),{
             'Matricula':'A01206199'})
        self.assertEqual(resp.status_code, 302)
        Cliente_acum = Cliente.objects.filter(Matricula='A01206199').count()
        self.assertEqual(Cliente_acum, 1)
        respm = self.client.post(reverse('prospectos:editar_cliente', kwargs={'id':1}),{
             'Matricula':'A01206198'})
        self.assertEqual(respm.status_code, 302)
        Cliente_mod = Cliente.objects.filter(Matricula='A01206198').count()
        self.assertEqual(Cliente_mod, 1)

    #ACCEPTANCE CRITERIA: 31.2
    def test_validar_campos(self):
         resp = self.client.post(reverse('prospectos:crear_cliente', kwargs={'id':1}),{
             'rfc':'RODR621124FY9'})
         self.assertEqual(resp.status_code, 200)
         self.assertEqual(resp.context['Error'],'Forma invalida, favor de revisar sus respuestas de nuevo')



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
    def test_crear_empresa(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'),{
            'Nombre':'ITESM',
            'Telefono1':'4422232226',
            'Email1':'escuela@itesm.com',
            'Razon_Social':'Escuela'})
        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(resp.context['empresas'],['<Empresa: ITESM>'])

    #ACCEPTANCE CRITERIA: 13.3
    def test_validar_campos(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'),{
            'Telefono1':'4422232226',
            'Email1':'correo@itesm.com',
            'Razon_Social':'Escuela'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['Error'],'Forma invalida, favor de revisar sus respuestas de nuevo')

    #ACCEPTANCE CRITERIA: 13.4
    def test_validar_tipo_de_dato(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'),{
            'Nombre':'ITESM',
            'Telefono1':'ABC',
            'Email1':'correo@itesm.com',
            'Razon_Social':'Escuela'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['Error'],'Forma invalida, favor de revisar sus respuestas de nuevo')

    #ACCEPTANCE CRITERIA: 13.6
    # def test_ac_13_6(self):
    #     Empresa.objects.create(
    #         Nombre='ITESM',
    #         Telefono1='4422232226',
    #         Email1='correo@itesm.com',
    #         Direccion=Lugar.objects.get(Calle='Paraiso'),
    #         Razon_Social='Escuela'
    #     )
    #     resp = self.client.post(reverse('prospectos:crear_empresa'),{
    #         'Nombre':'ITESM',
    #         'Telefono1':'4422232226',
    #         'Email1':'correo@itesm.com',
    #         'Razon_Social':'Escuela'})
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertEqual(resp.context['Error'],'Forma invalida, favor de revisar sus respuestas de nuevo')

    #ACCEPTANCE CRITERIA 14.1, 14.2
    def test_editar_empresa(self):
        Empresa.objects.create(
            id= '2',
            Nombre='ITESM',
            Contacto1='Lynda',
            Telefono1='4423367895',
            Puesto1='Recursos Humanos',
            Email1='correo@itesm.com',
            Direccion=Lugar.objects.get(Calle='Paraiso'),
            Razon_Social='Escuela'
        )
        resp = self.client.post(reverse('prospectos:editar_empresa', kwargs={'id': 2}),{
            'Nombre': 'ITESO', 'Contacto1': 'Lynda Brenda',
            'Telefono1': '4423367898', 'Puesto1': 'RH','Direccion':Lugar.objects.get(Calle='Paraiso'),
            'Email1':'lyndab@itesm.com',
            'Razon_Social': 'Escuela'
        },follow=True)
        actualizado = Empresa.objects.get(id=2)
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(actualizado, 'ITESM')

    def test_baja_empresas(self):
        Empresa.objects.create(
            id= '2',
            Nombre='ITESM',
            Contacto1='Lynda',
            Telefono1='4423367895',
            Puesto1='Recursos Humanos',
            Email1='correo@itesm.com',
            Direccion=Lugar.objects.get(Calle='Paraiso'),
            Razon_Social='Escuela'
        )
        resp = self.client.post(reverse('prospectos:baja_empresas', kwargs={'id': 2}),follow=True)
        actualizado = Empresa.objects.get(id=2)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(actualizado.Activo, False)

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
                Activo=True,
            )

    #Acceptance citeria: 7.1
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/prospectos/')
        self.assertEqual(resp.status_code, 200)

    def test_view_prospectos_20(self):
        resp = self.client.get(reverse('prospectos:lista_prospectos_inactivo'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['prospectos']),20)

    #Acceptance criteria 8.1
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('prospectos:lista_prospectos_inactivo'))
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
            Activo=True,
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
            Activo=True,
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
                Activo=True,
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
            Activo=True,
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
    #Acceptance Criteria 8.1
    def test_baja_prospecto(self):
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
            Activo=True,
        )
        resp = self.client.post(reverse('prospectos:baja_prospecto', kwargs={'id': 1}),follow=True)
        actualizado = Prospecto.objects.get(id=1)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(actualizado.Activo, False)

class ActividadTest(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
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
            Activo=True,
        )
        evento = Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')
        curso = Curso.objects.create(Nombre='CursoPrueba', Evento=evento, Fecha='2018-03-16', Direccion='Calle', Descripcion='Evento de marzo', Costo=1000)
        relacion = ProspectoEvento.objects.create(Prospecto=prospecto,Curso=curso,Interes='ALTO',FlagCADHU=False)

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

    def test_ac_12_3(self):
        act = Actividad.objects.get_or_create(
            titulo= 'Llamada con el prospecto',
            fecha= datetime.datetime.now().date(),
            notas= 'Llamada con el prosecto',
            prospecto_evento= 1,
            terminado=False,
        )
        resp = self.client.post(reverse('prospectos:estado_actividad',kwargs={'id':1}))
        self.assertEqual(act.terminado, True)

    def test_ac_12_4(self):
        act = Actividad.objects.get_or_create(
            titulo= 'Llamada con el prospecto',
            fecha= datetime.datetime.now().date(),
            notas= 'Llamada con el prosecto',
            prospecto_evento= 1,
            terminado=False,
        )
        resp = self.client.post(reverse('prospectos:estado_actividad',kwargs={'id':1}))
        self.assertEqual(act.terminado, True)


class CargaMasivaTest(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        lugar, created = Lugar.objects.get_or_create(
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
            Nombre='Alejandro',
            Apellidos='Salmon FD',
            Telefono_Casa='4422232226',
            Telefono_Celular='4422580662',
            Email='asalmon@cadhu.com',
            Direccion=lugar,
            Metodo_Captacion='Facebook',
            Estado_Civil='Soltero',
            Ocupacion='Estudiante',
            Hijos=1,
            Activo=True,
        )
        prospecto2 = Prospecto.objects.create(
            Nombre=' Alejandro',
            Apellidos='Salmon FD',
            Telefono_Casa='4422232226',
            Telefono_Celular='4422580662',
            Email='prospecto2@cadhu.com',
            Direccion=lugar,
            Metodo_Captacion='Facebook',
            Estado_Civil='Soltero',
            Ocupacion='Estudiante',
            Hijos=1,
            Activo=True,
        )
        evento = Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')
        curso = Curso.objects.create(Nombre='CursoPrueba', Evento=evento, Fecha='2018-03-16', Direccion='Calle', Descripcion='Evento de marzo', Costo=1000)
        relacion = ProspectoEvento.objects.create(Prospecto=prospecto, Curso=curso, Interes='ALTO', FlagCADHU=False)

    # ACCEPTANCE CRITERIA: 43.1
    def test_ac_43_1(self):
        curso = Curso.objects.get(Nombre='CursoPrueba').id
        csv = 'Nombre,Apellidos,Email,Telefono casa,Telefono celular,Metodo captacion,Estado civil,Ocupacion,Hijos,Recomendacion,Pais,Estado,Ciudad,Colonia,Calle,Numero exterior,Numero interior,Codigo postal,ID curso' \
              '\n Alejandro,Salmon FD,mancha@cadhu.com,4422232226,4422580662,Facebook,Soltero,Estudiante,1,,Mexico,Queretaro,Queretaro,Satelite,Paraiso,38,,76125,'+str(curso)
        with open('test.csv', 'w') as f:
            f.write(csv)
            f.close()
        archivo = open('test.csv', 'r')
        post = {'archivo': archivo}
        resp = self.client.post(reverse('prospectos:carga'), post)
        archivo.close()
        os.remove('test.csv')
        os.remove('static/files/resultado.xls')
        prospecto = Prospecto.objects.get(Email='mancha@cadhu.com')
        prospecto2 = Prospecto.objects.get(Email='prospecto2@cadhu.com')
        prospecto_count = Prospecto.objects.filter(id=prospecto.id).count()
        prospecto_rel = ProspectoEvento.objects.filter(Prospecto=prospecto).count()
        prospecto2_rel = ProspectoEvento.objects.filter(Prospecto_id=prospecto2.id).count()
        self.assertEqual(prospecto_count, 1)
        self.assertEqual(prospecto_rel, 1)
        self.assertEqual(prospecto2_rel, 0)

    #ACCEPTANCE CRITERIA: 43.2
    # def test_ac_43_2(self):
    #     curso = Curso.objects.get(Nombre='CursoPrueba').id
    #     csv = 'Nombre,Apellidos,Email,Telefono casa,Telefono celular,Metodo captacion,Estado civil,Ocupacion,Hijos,Recomendacion,Pais,Estado,Ciudad,Colonia,Calle,Numero exterior,Numero interior,Codigo postal,ID curso' \
    #           '\n Alejandro,Salmon FD,prospecto2@cadhu.com,4422232226,4422580662,Facebook,Soltero,Estudiante,1,,Mexico,Queretaro,Queretaro,Satelite,Paraiso,38,,76125,'+str(curso)
    #     with open('test.csv', 'w') as f:
    #         f.write(csv)
    #         f.close()
    #     archivo = open('test.csv', 'r')
    #     post = {'archivo': archivo}
    #     resp = self.client.post(reverse('prospectos:carga'), post)
    #     archivo.close()
    #     os.remove('test.csv')
    #     os.remove('static/files/resultado.xls')
    #     prospecto = Prospecto.objects.get(Email='prospecto2@cadhu.com')
    #     prospecto_count = Prospecto.objects.filter(id=prospecto.id).count()
    #     prospecto_rel = ProspectoEvento.objects.filter(Prospecto=prospecto).count()
    #     self.assertEqual(prospecto_count, 1)
    #     self.assertEqual(prospecto_rel, 1)

    #ACCEPTANCE CRITERIA: 43.3
    def test_ac_43_3(self):
        curso = Curso.objects.get(Nombre='CursoPrueba').id
        csv = 'Nombre,Apellidos,Email,Telefono casa,Telefono celular,Metodo captacion,Estado civil,Ocupacion,Hijos,Recomendacion,Pais,Estado,Ciudad,Colonia,Calle,Numero exterior,Numero interior,Codigo postal,ID curso' \
              '\n Alejandro,Salmon FD,asalmon@cadhu.com,4422232226,4422580662,Facebook,Soltero,Estudiante,1,,Mexico,Queretaro,Queretaro,Satelite,Paraiso,38,,76125,'+str(curso)
        prospecto = Prospecto.objects.get(Email='asalmon@cadhu.com')
        prospecto_count_antes = Prospecto.objects.filter(id=prospecto.id).count()
        prospecto_rel_antes = ProspectoEvento.objects.filter(Prospecto=prospecto).count()
        with open('test.csv', 'w') as f:
            f.write(csv)
            f.close()
        archivo = open('test.csv', 'r')
        post = {'archivo': archivo}
        resp = self.client.post(reverse('prospectos:carga'), post)
        archivo.close()
        os.remove('test.csv')
        os.remove('static/files/resultado.xls')
        prospecto = Prospecto.objects.get(Email='asalmon@cadhu.com')
        prospecto_count = Prospecto.objects.filter(id=prospecto.id).count()
        prospecto_rel = ProspectoEvento.objects.filter(Prospecto=prospecto).count()
        self.assertEqual(prospecto_count, prospecto_count_antes)
        self.assertEqual(prospecto_rel, prospecto_rel_antes)

    #ACCEPTANCE CRITERIA: 43.4
    def test_ac_43_4(self):
        curso = Curso.objects.get(Nombre='CursoPrueba').id
        csv = 'Nombre,Apellidos,Email,Telefono casa,Telefono celular,Metodo captacion,Estado civil,Ocupacion,Hijos,Recomendacion,Pais,Estado,Ciudad,Colonia,Calle,Numero exterior,Numero interior,Codigo postal,ID curso' \
              '\n Pedro,Salmon FD,asalmon@cadhu.com,1234567890,4422580662,Facebook,Soltero,Estudiante,1,,Mexico,Queretaro,Queretaro,Satelite,Paraiso,38,,76125,'+str(curso)
        with open('test.csv', 'w') as f:
            f.write(csv)
            f.close()
        archivo = open('test.csv', 'r')
        post = {'archivo': archivo}
        resp = self.client.post(reverse('prospectos:carga'), post)
        archivo.close()
        os.remove('test.csv')
        os.remove('static/files/resultado.xls')
        prospecto = Prospecto.objects.get(Email='asalmon@cadhu.com')
        prospecto_count = Prospecto.objects.filter(id=prospecto.id).count()
        self.assertEqual(prospecto_count, 1)

    #ACCEPTANCE CRITERIA: 43.5
    def test_ac_43_5(self):
        curso = Curso.objects.get(Nombre='CursoPrueba').id
        csv = 'Nombre,Apellidos,Email,Telefono casa,Telefono celular,Metodo captacion,Estado civil,Ocupacion,Hijos,Recomendacion,Pais,Estado,Ciudad,Colonia,Calle,Numero exterior,Numero interior,Codigo postal,ID curso' \
              '\n Alejandro,Salmon FD,prospecto2@cadhu.com,4422232226,4422580662,Facebook,Soltero,Estudiante,1,,Mexico,Queretaro,Queretaro,Satelite,Paraiso,38,,76125,102'
        with open('test.csv', 'w') as f:
            f.write(csv)
            f.close()
        archivo = open('test.csv', 'r')
        post = {'archivo': archivo}
        resp = self.client.post(reverse('prospectos:carga'), post)
        archivo.close()
        os.remove('test.csv')
        os.remove('static/files/resultado.xls')
        prospecto = Prospecto.objects.get(Email='prospecto2@cadhu.com')
        prospecto_count = Prospecto.objects.filter(id=prospecto.id).count()
        prospecto_rel = ProspectoEvento.objects.filter(Prospecto=prospecto).count()
        self.assertEqual(prospecto_count, 1)
        self.assertEqual(prospecto_rel, 0)


class PagoTest(TestCase):

    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        lugar = Lugar.objects.create( Calle='Paraiso', Numero_Interior='', Numero_Exterior='38', Colonia='Satelite', Estado='Queretaro', Ciudad='Queretaro', Pais='Mexico', Codigo_Postal='76125' )
        prospecto = Prospecto.objects.create( Nombre='Pablo', Apellidos='Martinez Villareal', Telefono_Casa='4422232226', Telefono_Celular='4422580662', Email='asdas@gmail.com', Direccion= lugar, Ocupacion='Estudiante', Activo=True)
        evento = Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')
        curso = Curso.objects.create(Nombre='Curso', Evento= evento, Fecha_Inicio='2018-03-16', Fecha_Fin='2018-03-16', Direccion='Calle', Descripcion='Evento de marzo', Costo=1000)
        prospecto_evento = ProspectoEvento.objects.create(Fecha='2018-03-15', Interes='ALTO', FlagCADHU=False, status='INTERESADO', Curso_id= curso.id, Prospecto_id = prospecto.id)
        # print("IDPE:")
        # print(prospecto_evento.id)
        # print("ID:")
        # print(prospecto.id)
        pago = Pago.objects.create(fecha='2018-03-15', monto=200, referencia="1651", prospecto_evento_id = prospecto_evento.id)
        cliente = Cliente.objects.create(Matricula='asd123', Fecha='2018-03-15', ProspectoEvento_id = prospecto_evento.id)

    def test_ac_42_1(self):

        resp = self.client.get(reverse('prospectos:lista_pagos', kwargs={'id': 5, 'idPE': 2}))
        # return redirect(reverse('basic_app:classroom_list', kwargs={'pk': user.id}))
        # resp = self.client.post(reverse('prospectos:baja_prospecto', kwargs={'id': 1})
        self.assertEqual(resp.status_code, 200)
        # self.assertTemplateUsed(resp, 'pagos/lista_pagos.html')

    def test_ac_41_2(self):
        resp = self.client.post(reverse('prospectos:nuevo_pago', kwargs={'idPE': 2}),{
            "fecha": '2018-03-15',
            "monto": 200,
            "referencia": "1651",
            "prospecto_evento_id": 2
        }, follow=True)
        self.assertEqual(resp.status_code, 200)

    # def test_view_crear_curso(self):
    #     evento = Evento.objects.create(Nombre='Mi Evento 2', Descripcion='Este es el evento de pruebas automoatizadas.')
    #     resp = self.client.post('/cursos/nuevo_curso',  {
    #         'Nombre': 'Curso',
    #         'Evento': evento,
    #         'Fecha_Inicio': '2018-03-16',
    #         'Fecha_Fin': '2018-03-16',
    #         'Direccion': 'Calle',
    #         'Descripcion': 'Evento de marzo',
    #         'Costo': 1000},
    #         follow=True
    #     )
    #     self.assertEqual(resp.status_code, 200)
