from django.test import TestCase, client
from django.urls import reverse
from eventos.models import Evento
from cursos.models import Curso
from django.db.models import QuerySet
from .models import Prospecto, Lugar, Actividad, Empresa, ProspectoEvento, Cliente, Pago
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.contrib.messages import get_messages
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
        cls.prospecto = Prospecto.objects.create(id=1,nombre='Pablo', apellidos='Martinez Villareal', email='pmartinez@gmail.com')
        cls.evento = Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')
        cls.curso = Curso.objects.create(Nombre='CursoPrueba', Evento=cls.evento, Direccion='Calle', Costo=1000)
        cls.relacion = ProspectoEvento.objects.create(Prospecto=cls.prospecto, Curso=cls.curso, Interes='ALTO', FlagCADHU=False)
        cls.pago = Pago.objects.create(monto=500, prospecto_evento=cls.relacion)
        cls.cliente = Cliente.objects.create(ProspectoEvento=cls.relacion, matricula='a01206199')

    #ACCEPTANCE CRITERIA: 30.1
    def test_eliminar_cliente(self):
        # resp = self.client.post(reverse('prospectos:crear_cliente', kwargs={'id': self.pago.id}), {
        #      'matricula': 'A016197'})
        # self.assertEqual(resp.status_code, 302)
        # cliente_acum = Cliente.objects.filter(matricula='A016197').count()
        # self.assertEqual(cliente_acum, 1)
        respm = self.client.post(reverse('prospectos:eliminar_cliente', kwargs={'id': self.relacion.id}), {
             'matricula': 'a01206199'})
        cliente_eliminado = Cliente.objects.filter(matricula='a01206199').count()
        self.assertEqual(cliente_eliminado, 0)

    #ACCEPTANCE CRITERIA: 31.1
    def test_crear_cliente(self):
        resp = self.client.post(reverse('prospectos:crear_cliente', kwargs={'id': self.pago.id}), {
             'matricula': 'A01206199'})
        self.assertEqual(resp.status_code, 302)
        cliente_acum = Cliente.objects.filter(matricula='A01206199').count()
        self.assertEqual(cliente_acum, 1)

    #ACCEPTANCE CRITERIA: 31.1
    def test_editar_cliente(self):
        respm = self.client.post(reverse('prospectos:editar_cliente', kwargs={'id': self.cliente.id}), {
             'matricula': 'A01206198'})
        self.assertEqual(respm.status_code, 302)
        cliente_mod = Cliente.objects.filter(matricula='A01206198').count()
        self.assertEqual(cliente_mod, 1)

    #ACCEPTANCE CRITERIA: 31.2
    def test_validar_campos(self):
         resp = self.client.post(reverse('prospectos:crear_cliente', kwargs={'id':self.cliente.id}),{
             'rfc':'RODR621124FY9'})
         self.assertEqual(resp.status_code, 200)
         self.assertEqual(resp.context['Error'], 'Forma invalida, favor de revisar sus respuestas de nuevo')

    #ACCEPTANCE CRITERIA: 18.1
    def test_baja_cliente(self):
        prospecto, created = Prospecto.objects.get_or_create(Nombre='Pablo', Apellidos='Martinez Villareal',
                                                             Email='pmartinez@gmail.com')
        resp = self.client.post(reverse('prospectos:crear_cliente', kwargs={'id': self.pago.id}), {
            'matricula': 'A01206199'})
        self.assertEqual(resp.status_code, 302)
        resp2 = self.client.post(reverse('prospectos:baja_cliente', kwargs={'id': 1}),follow=True)
        actualizado = Cliente.objects.get(id=1)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(actualizado.Activo, False)

    #Acceptance citeria: 38.1
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/clientes/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('prospectos:lista_clientes'))
        self.assertEqual(resp.status_code, 200)


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
        Empresa.objects.create(
            nombre='EDECONSA',
            Contacto1='Alejandro Salmon',
            Contacto2='Marco Luna',
            Telefono1='4423839974',
            Telefono2='4424738847',
            Email1='asalmon@gmail.com',
            Email2='mluna@gmail.com',
            Puesto1='Presidente',
            Puesto2='Conserje',
            Razon_Social='Constructora',
            Direccion=Lugar.objects.get(Calle='Paraiso'),
            Activo=True
        )

    #ACCEPTANCE CRITERIA: 13.2
    def test_crear_empresa(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'),{
            'nombre':'ITESM',
            'Telefono1':'4422232226',
            'Email1':'escuela@itesm.com',
            'Razon_Social':'Escuela'})
        itesm=Empresa.objects.filter(nombre='ITESM').count()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(itesm, 1)

    #ACCEPTANCE CRITERIA: 13.3
    def test_validar_campos(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'),{
            'Telefono1': '4422232226',
            'Email1': 'correo@itesm.com',
            'Razon_Social': 'Escuela'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['Error'],'Forma invalida, favor de revisar sus respuestas de nuevo')

    #ACCEPTANCE CRITERIA: 13.4
    def test_validar_tipo_de_dato(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'),{
            'nombre': 'ITESM',
            'Telefono1': 'ABC',
            'Email1': 'correo@itesm.com',
            'Razon_Social': 'Escuela'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['Error'], 'Forma invalida, favor de revisar sus respuestas de nuevo')

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
            id=3,
            nombre='ITESM',
            Contacto1='Lynda',
            Telefono1='4423367895',
            Puesto1='Recursos Humanos',
            Email1='correo@itesm.com',
            Direccion=Lugar.objects.get(Calle='Paraiso'),
            Razon_Social='Escuela'
        )
        resp = self.client.post(reverse('prospectos:editar_empresa', kwargs={'id': 3}), {
            'nombre': 'ITESO', 'Contacto1': 'Lynda Brenda',
            'Telefono1': '4423367898', 'Puesto1': 'RH','Direccion': Lugar.objects.get(Calle='Paraiso'),
            'Email1':'lyndab@itesm.com',
            'Razon_Social': 'Escuela'
        },follow=True)
        actualizado = Empresa.objects.get(id=3)
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(actualizado, 'ITESM')

    #ACCEPTANCE CRITERIA: 15.1
    def test_empresa_info(self):
        resp = self.client.get(reverse('prospectos:empresa_info', kwargs={'id': 1}), {
            'nombre': 'EDECONSA','Contacto1':'Alejandro Salmon'
        }, follow=True)
        self.assertEqual(resp.status_code, 200)

    #ACCEPTANCE CRITERIA: 18.1
    def test_baja_empresas(self):
        Empresa.objects.create(
            id=2,
            nombre='ITESM',
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
        cls.number_of_prospectos = 20
        cls.N = 10
        Lugar.objects.create(
            calle='Paraiso',
            numero_interior='',
            numero_exterior='38',
            colonia='Satelite',
            estado='Queretaro',
            ciudad='Queretaro',
            pais='Mexico',
            codigo_postal='76125'
        )
        for prospecto in range(cls.number_of_prospectos):
            Prospecto.objects.create(
                nombre='Pablo',
                apellidos='Martinez Villareal',
                telefono_casa='4422232226',
                telefono_celular='4422580662',
                email=''.join([random.choice(string.ascii_letters + string.digits)for n in range(32)]) + '@gmail.com',
                direccion=Lugar.objects.get(calle='Paraiso'),
                ocupacion='Estudiante',
                activo=True,
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
            calle='Paraiso',
            numero_interior='',
            numero_exterior='38',
            colonia='Satelite',
            estado='Queretaro',
            ciudad='Queretaro',
            pais='Mexico',
            codigo_postal='76125'
        )
        Prospecto.objects.create(
            nombre='Pablo',
            apellidos='Martinez Villareal',
            telefono_casa='4422232226',
            telefono_celular='4422580662',
            email='pmartinez@gmail.com',
            direccion=Lugar.objects.get(calle='Paraiso'),
            metodo_captacion='Facebook',
            estado_civil='Soltero',
            ocupacion='Estudiante',
            hijos=1,
            activo=True,
        )

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
            calle='Lourdes',
            numero_interior='5',
            numero_exterior='73',
            colonia='Satelite',
            estado='Queretaro',
            ciudad='Queretaro',
            pais='Mexico',
            codigo_postal='76125'
        )
        Prospecto.objects.create(
            nombre='Pablo',
            apellidos='Martinez Villareal',
            telefono_casa='4422232226',
            telefono_celular='4422580662',
            email='pmartinez@gmail.com',
            direccion=Lugar.objects.get(calle='Lourdes'),
            metodo_captacion='Facebook',
            estado_civil='Soltero',
            ocupacion='Estudiante',
            hijos=1,
            activo=True,
        )
        Prospecto_acum = Prospecto.objects.filter(email='a01209537@itesm.mx').count()
        self.assertEqual(Prospecto_acum, 1)

    def test_prospecto_mismo_mail(self):
        try:
            Prospecto.objects.create(
                nombre='Pablo',
                apellidos='Martinez Villareal',
                telefono_casa='4422232226',
                telefono_celular='4422580662',
                email='pmartinez@gmail.com',
                direccion=Lugar.objects.get(calle='Paraiso'),
                metodo_captacion='Facebook',
                estado_civil='Soltero',
                ocupacion='Estudiante',
                hijos=1,
                activo=True,
            )
            Prospecto_acum = Prospecto.objects.all().count()
            self.assertEqual(Prospecto_acum, 0)
        except:
            Prospecto_acum = Prospecto.objects.all().count()
            self.assertEqual(Prospecto_acum, 1)

    # ID_AC 4.1, 4.2
    def test_editar_prospecto(self):
        Lugar.objects.create(
            calle='Lourdes',
            numero_interior='4',
            numero_exterior='105',
            colonia='Satelite',
            estado='Queretaro',
            ciudad='Queretaro',
            pais='Mexico',
            codigo_postal='76125'
        )
        Prospecto.objects.create(
            id='1',
            nombre='Marco Antonio',
            apellidos='Luna Calvillo',
            telefono_casa='4422232226',
            telefono_celular='4422580662',
            email='a01209537@itesm.mx',
            direccion=Lugar.objects.get(calle='Lourdes'),
            metodo_captacion='Facebook',
            estado_civil='Soltero',
            ocupacion='Estudiante',
            hijos=1,
            activo=True,
        )
        resp = self.client.post(reverse('prospectos:editar_prospecto', kwargs={'id': 1}),{
            'nombre': 'Luis Alfredo', 'apellidos': 'Rodriguez Santos',
            'telefono_casa': '4422232226', 'telefono_celular': '4422580662','direccion':Lugar.objects.get(calle='Lourdes'),
            'email': 'a01209537@itesm.mx', 'metodo_captacion': 'Facebook',
            'estado_civil': 'SOLTERO', 'ocupacion': 'Estudiante', 'hijos': 1
        },follow=True)
        actualizado = Prospecto.objects.get(id=1)
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(actualizado, 'Marco Antonio Luna Calvillo')

    #Acceptance Criteria 8.1
    def test_baja_prospecto(self):
        Lugar.objects.create(
            calle='Lourdes',
            numero_interior='4',
            numero_exterior='105',
            colonia='Satelite',
            estado='Queretaro',
            ciudad='Queretaro',
            pais='Mexico',
            codigo_postal='76125'
        )
        Prospecto.objects.create(
            id='1',
            nombre='Marco Antonio',
            apellidos='Luna Calvillo',
            telefono_casa='4422232226',
            telefono_celular='4422580662',
            email='a01209537@itesm.mx',
            direccion=Lugar.objects.get(calle='Lourdes'),
            metodo_captacion='Facebook',
            estado_civil='Soltero',
            ocupacion='Estudiante',
            hijos=1,
            activo=True,
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
        cls.lugar = Lugar.objects.create(
            Calle='Paraiso',
            Numero_Interior='',
            Numero_Exterior='38',
            Colonia='Satelite',
            Estado='Queretaro',
            Ciudad='Queretaro',
            Pais='Mexico',
            Codigo_Postal='76125'
        )
        cls.prospecto = Prospecto.objects.create(
            Nombre='Pablo',
            Apellidos='Martinez Villareal',
            Telefono_Casa='4422232226',
            Telefono_Celular='4422580662',
            Email='pmartinez@gmail.com',
            Direccion=cls.lugar,
            Metodo_Captacion='Facebook',
            Estado_Civil='Soltero',
            Ocupacion='Estudiante',
            Hijos=1,
            Activo=True,
        )
        cls.evento = Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')
        cls.curso = Curso.objects.create(Nombre='Curso', Evento=cls.evento, Fecha_Inicio='2018-03-16', Fecha_Fin='2018-03-16', Direccion='Calle', Descripcion='Evento de marzo', Costo=1000)
        cls.relacion = ProspectoEvento.objects.create(Prospecto=cls.prospecto, Curso=cls.curso, Interes='ALTO', FlagCADHU=False)
        cls.actFalse = Actividad.objects.create(titulo='Actividad False', fecha=datetime.datetime.now().date(), notas='Llamada con el prosecto', prospecto_evento=cls.relacion, terminado=False)
        cls.actTrue = Actividad.objects.create(titulo='Actividad True', fecha=datetime.datetime.now().date(), notas='Llamada con el prosecto', prospecto_evento=cls.relacion, terminado=True)


    # ACCEPTANCE CRITERIA: 12.1
    def test_ac_12_1(self):
        resp = self.client.post(reverse('prospectos:crear_actividad',kwargs={'id': self.relacion.id}), {
            'titulo': 'Llamada con el prospecto',
            'fecha': datetime.datetime.now().date(),
            'notas': 'Llamada con el prosecto',
            'prospecto_evento': self.relacion})
        act_count = Actividad.objects.all().count()
        self.assertEqual(act_count, 3)

    #ACCEPTANCE CRITERIA: 12.2
    def test_ac_12_2(self):
        resp = self.client.post(reverse('prospectos:crear_actividad', kwargs={'id': self.relacion.id}), {
            'titulo': 'Llamada con el prospecto',
            'fecha': False,
            'hora': 'Hora',
            'notas': 'Llamada con el prosecto'
        })
        mensaje = get_messages(resp)
        self.assertEqual(resp.context['Error'], 'Forma inválida')

    def test_ac_12_3(self):
        resp = self.client.post(reverse('prospectos:estado_actividad', kwargs={'id': self.actFalse.id}))
        self.assertEqual(self.actFalse.terminado, False)

    def test_ac_12_4(self):
        resp = self.client.post(reverse('prospectos:estado_actividad', kwargs={'id': self.actTrue.id}))
        self.assertEqual(self.actTrue.terminado, True)


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
            calle='Paraiso',
            numero_interior='',
            numero_exterior='38',
            colonia='Satelite',
            estado='Queretaro',
            ciudad='Queretaro',
            pais='Mexico',
            codigo_postal='76125'
        )
        prospecto = Prospecto.objects.create(
            nombre='Alejandro',
            apellidos='Salmon FD',
            telefono_casa='4422232226',
            telefono_celular='4422580662',
            email='asalmon@cadhu.com',
            direccion=lugar,
            metodo_captacion='Facebook',
            estado_civil='Soltero',
            ocupacion='Estudiante',
            hijos=1,
            activo=True,
        )
        prospecto2 = Prospecto.objects.create(
            nombre=' Alejandro',
            apellidos='Salmon FD',
            telefono_casa='4422232226',
            telefono_celular='4422580662',
            email='prospecto2@cadhu.com',
            direccion=lugar,
            metodo_captacion='Facebook',
            estado_civil='Soltero',
            ocupacion='Estudiante',
            hijos=1,
            activo=True,
        )
        evento = Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')
        curso = Curso.objects.create(Nombre='CursoPrueba', Evento=evento, Fecha_Inicio='2018-03-16', Fecha_Fin='2018-03-16', Direccion='Calle', Descripcion='Evento de marzo', Costo=1000)
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
        prospecto = Prospecto.objects.get(email='mancha@cadhu.com')
        prospecto2 = Prospecto.objects.get(email='prospecto2@cadhu.com')
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
        prospecto = Prospecto.objects.get(email='asalmon@cadhu.com')
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
        prospecto = Prospecto.objects.get(email='asalmon@cadhu.com')
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
        prospecto = Prospecto.objects.get(email='asalmon@cadhu.com')
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
        prospecto = Prospecto.objects.get(email='prospecto2@cadhu.com')
        prospecto_count = Prospecto.objects.filter(id=prospecto.id).count()
        prospecto_rel = ProspectoEvento.objects.filter(Prospecto=prospecto).count()
        self.assertEqual(prospecto_count, 1)
        self.assertEqual(prospecto_rel, 0)


class VistaCursosTest(TestCase):
    def SetUP(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        cls.lugar = Lugar.objects.create(Calle='Paraiso', Numero_Interior='', Numero_Exterior='38', Colonia='Satelite',
                                     Estado='Queretaro', Ciudad='Queretaro', Pais='Mexico', Codigo_Postal='76125')
        cls.prospecto = Prospecto.objects.create(Nombre='Pablo', Apellidos='Martinez Villareal', Telefono_Casa='4422232226',
                                             Telefono_Celular='4422580662', Email='asdas@gmail.com', Direccion=cls.lugar,
                                             Ocupacion='Estudiante', Activo=True)
        cls.evento = Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')
        cls.curso = Curso.objects.create(Nombre='Curso', Evento=cls.evento, Fecha_Inicio='2018-03-16', Fecha_Fin='2018-03-16',
                                     Direccion='Calle', Descripcion='Evento de marzo', Costo=1000)
        cls.prospecto_evento = ProspectoEvento.objects.create(Fecha='2025-03-15', Interes='ALTO', FlagCADHU=False,
                                                          status='INTERESADO', Curso_id=cls.curso.id,
                                                          Prospecto_id=cls.prospecto.id)
        cls.pago = Pago.objects.create(fecha='2018-03-15', monto=200, referencia="1651",
                                   prospecto_evento_id=cls.prospecto_evento.id, comentarios="comentario de prueba")
        cls.cliente = Cliente.objects.create(Matricula='asd123', Fecha='2018-03-15', ProspectoEvento_id=cls.prospecto_evento.id)

    def testListaClientes(self):
        resp = self.client.post(reverse('prospectos:info_curso', kwargs={'id': self.curso.id}),)
        prospectos_lista = Prospecto.objects.filter(prospectoevento__Curso=self.curso)
        clientes = []
        prospectos = []
        for prospecto in prospectos_lista:
            if prospecto.prospectoevento.pago_set:
                clientes.append(prospecto)
            else:
                prospectos.append(prospecto)
        self.assertEqual(resp.context['prospectos'], prospectos)
        self.assertEqual(resp.context['clientes'], clientes)


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
        prospecto_evento = ProspectoEvento.objects.create(Fecha='2025-03-15', Interes='ALTO', FlagCADHU=False, status='INTERESADO', Curso_id= curso.id, Prospecto_id = prospecto.id)
        pago = Pago.objects.create(fecha='2018-03-15', monto=200, referencia="1651", prospecto_evento_id=prospecto_evento.id, comentarios="comentario de prueba", tipo_pago="Efectivo")
        cliente = Cliente.objects.create(matricula='asd123', Fecha='2018-03-15', ProspectoEvento_id=prospecto_evento.id)

    def test_ac_42_1(self):
        idPE = ProspectoEvento.objects.get(Fecha='2025-03-15').id
        resp = self.client.get(reverse('prospectos:lista_pagos', kwargs={'idPE': idPE}))
        # return redirect(reverse('basic_app:classroom_list', kwargs={'pk': user.id}))
        # resp = self.client.post(reverse('prospectos:baja_prospecto', kwargs={'id': 1})
        self.assertEqual(resp.status_code, 200)
        # self.assertTemplateUsed(resp, 'pagos/lista_pagos.html')

    def test_ac_41_2(self):
        idPE = ProspectoEvento.objects.get(Fecha='2025-03-15').id
        resp = self.client.post(reverse('prospectos:nuevo_pago', kwargs={'idPE': idPE}), {
            "fecha": '2025-03-15',
            "monto": 200,
            "referencia": "1651",
            "prospecto_evento_id": idPE,
            "comentarios": "comentario de prueba",
            "tipo_pago": "Efectivo"
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
