from django.test import TestCase
from cursos.models import Curso
from grupos.models import Grupo
from .models import Prospecto, Lugar, Actividad, Empresa, ProspectoGrupo, Cliente, Pago
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
        usuario1 = User.objects.create_user(username='testuser1', password='12345', is_superuser=True)
        usuario1.save()
        self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        cls.prospecto = Prospecto.objects.create(id=1, nombre='Pablo', apellidos='Martinez Villareal',
                                                 email='pmartinez@gmail.com')
        cls.curso = Curso.objects.create(nombre='Mi Curso', descripcion='Este es el curso de pruebas automoatizadas.')
        cls.grupo = Grupo.objects.create(nombre='CursoPrueba', curso=cls.curso, direccion='Calle', costo=1000)
        cls.relacion = ProspectoGrupo.objects.create(prospecto=cls.prospecto, grupo=cls.grupo, interes='ALTO',
                                                     flag_cadhu=False)
        cls.pago = Pago.objects.create(monto=500, prospecto_grupo=cls.relacion)
        cls.cliente = Cliente.objects.create(prospecto_grupo=cls.relacion, matricula='a01206199')

    # ACCEPTANCE CRITERIA: 31.1
    def test_crear_cliente(self):
        resp = self.client.post(reverse('prospectos:crear_cliente', kwargs={'pk': self.pago.id}),
                                {'matricula': 'A01206199'})
        self.assertEqual(resp.status_code, 302)
        cliente_acum = Cliente.objects.filter(matricula='A01206199').count()
        self.assertEqual(cliente_acum, 1)

    # ACCEPTANCE CRITERIA: 31.1
    def test_editar_cliente(self):
        respm = self.client.post(reverse('prospectos:editar_cliente', kwargs={'pk': self.relacion.id}),
                                 {'matricula': 'A01206198'})
        self.assertEqual(respm.status_code, 302)
        cliente_mod = Cliente.objects.filter(matricula='A01206198').count()
        self.assertEqual(cliente_mod, 1)

    # ACCEPTANCE CRITERIA: 31.2
    def test_validar_campos(self):
        resp = self.client.post(reverse('prospectos:crear_cliente', kwargs={'pk': self.pago.id}),
                                {'rfc': 'RODR621124FY9'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['Error'], 'Forma invalida, favor de revisar sus respuestas de nuevo')

    # ACCEPTANCE CRITERIA: 18.1
    def test_baja_cliente(self):
        resp = self.client.post(reverse('prospectos:crear_cliente', kwargs={'pk': self.pago.id}), {'matricula': 'A01206199'})
        self.assertEqual(resp.status_code, 302)
        resp2 = self.client.post(reverse('prospectos:baja_cliente', kwargs={'pk': self.cliente.id+1}), follow=True)
        actualizado = Cliente.objects.get(id=self.cliente.id+1)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(actualizado.activo, False)

    # ACCEPTANCE CRITERIA: 30.1
    def test_eliminar_cliente(self):
        self.client.post(reverse('prospectos:eliminar_cliente', kwargs={'pk': self.cliente.id}),
                         {'matricula': 'a01206199'})
        cliente_eliminado = Cliente.objects.filter(matricula='a01206199').count()
        self.assertEqual(cliente_eliminado, 0)


    # Acceptance citeria: 38.1
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/prospectos/clientes/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_exists_at_desired_location_2(self):
        resp = self.client.get(reverse('prospectos:lista_clientes'))
        self.assertEqual(resp.status_code, 200)


class EmpresaTest(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345', is_superuser=True)
        usuario1.save()
        self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):

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
        Empresa.objects.create(
            nombre='EDECONSA',
            contacto_1='Alejandro Salmon',
            contacto_2='Marco Luna',
            telefono_1='4423839974',
            telefono_2='4424738847',
            email_1='asalmon@gmail.com',
            email_2='mluna@gmail.com',
            puesto_1='Presidente',
            puesto_2='Conserje',
            razon_social='Constructora',
            direccion=Lugar.objects.get(calle='Paraiso'),
            activo=True
        )

    # ACCEPTANCE CRITERIA: 13.2
    def test_crear_empresa(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'), {
            'nombre': 'ITESM',
            'telefono_1': '4422232226',
            'email_1': 'escuela@itesm.com',
            'razon_social': 'Escuela'})
        itesm = Empresa.objects.filter(nombre='ITESM').count()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(itesm, 1)

    # ACCEPTANCE CRITERIA: 13.3
    def test_validar_campos(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'), {
            'telefono_1': '4422232226',
            'email_1': 'correo@itesm.com',
            'razon_social': 'Escuela'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['Error'], 'Forma invalida, favor de revisar sus respuestas de nuevo')

    # ACCEPTANCE CRITERIA: 13.4
    def test_validar_tipo_de_dato(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'), {
            'nombre': 'ITESM',
            'telefono_1': 'ABC',
            'email_1': 'correo@itesm.com',
            'razon_social': 'Escuela'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['Error'], 'Forma invalida, favor de revisar sus respuestas de nuevo')

    # ACCEPTANCE CRITERIA: 13.6
    # def test_ac_13_6(self):
    #     Empresa.objects.create(
    #         nombre='ITESM',
    #         telefono_1='4422232226',
    #         Email1='correo@itesm.com',
    #         direccion=Lugar.objects.get(calle='Paraiso'),
    #         razon_social='Escuela'
    #     )
    #     resp = self.client.post(reverse('prospectos:crear_empresa'),{
    #         'nombre':'ITESM',
    #         'telefono_1':'4422232226',
    #         'Email1':'correo@itesm.com',
    #         'razon_social':'Escuela'})
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertEqual(resp.context['Error'],'Forma invalida, favor de revisar sus respuestas de nuevo')

    # ACCEPTANCE CRITERIA 14.1, 14.2
    def test_editar_empresa(self):
        Empresa.objects.create(
            id=3,
            nombre='ITESM',
            contacto_1='Lynda',
            telefono_1='4423367895',
            puesto_1='Recursos Humanos',
            email_1='correo@itesm.com',
            direccion=Lugar.objects.get(calle='Paraiso'),
            razon_social='Escuela'
        )
        resp = self.client.post(reverse('prospectos:editar_empresa', kwargs={'pk': 3}), {
            'nombre': 'ITESO', 'contacto_1': 'Lynda Brenda',
            'telefono_1': '4423367898', 'puesto_1': 'RH', 'direccion': Lugar.objects.get(calle='Paraiso'),
            'email_1': 'lyndab@itesm.com',
            'razon_social': 'Escuela'
        }, follow=True)
        actualizado = Empresa.objects.get(id=3)
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(actualizado, 'ITESM')

    # ACCEPTANCE CRITERIA: 15.1
    def test_empresa_info(self):
        resp = self.client.get(reverse('prospectos:empresa_info', kwargs={'pk': 1}), {
            'nombre': 'EDECONSA', 'contacto_1': 'Alejandro Salmon'
        }, follow=True)
        self.assertEqual(resp.status_code, 200)

    # ACCEPTANCE CRITERIA: 18.1
    def test_baja_empresas(self):
        Empresa.objects.create(
            id=2,
            nombre='ITESM',
            contacto_1='Lynda',
            telefono_1='4423367895',
            puesto_1='Recursos Humanos',
            email_1='correo@itesm.com',
            direccion=Lugar.objects.get(calle='Paraiso'),
            razon_social='Escuela'
        )
        resp = self.client.post(reverse('prospectos:baja_empresas', kwargs={'pk': 2}), follow=True)
        actualizado = Empresa.objects.get(id=2)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(actualizado.activo, False)


class ProspectoListViewTest(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345', is_superuser=True)
        usuario1.save()
        self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        number_of_prospectos = 20
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
        for prospecto in range(0, number_of_prospectos):
            Prospecto.objects.create(
                nombre='Pablo',
                apellidos='Martinez Villareal',
                telefono_casa='4422232226',
                telefono_celular='4422580662',
                email=''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]) + '@gmail.com',
                direccion=Lugar.objects.get(calle='Paraiso'),
                ocupacion='Estudiante',
                activo=True,
            )
        for prospecto in range(0, number_of_prospectos):
            Prospecto.objects.create(
                nombre='Pablo',
                apellidos='Martinez Villareal',
                telefono_casa='4422232226',
                telefono_celular='4422580662',
                email=''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)]) + '@gmail.com',
                direccion=Lugar.objects.get(calle='Paraiso'),
                ocupacion='Estudiante',
                activo=False,
            )

    # Acceptance citeria: 7.1
    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/prospectos/')
        self.assertEqual(resp.status_code, 200)

    def test_view_prospectos_inactivos_20(self):
        resp = self.client.get(reverse('prospectos:lista_prospectos_inactivo'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['prospectos'].count(), 20)

    # Acceptance criteria 8.1
    def test_view_url_exists_at_desired_location_2(self):
        resp = self.client.get(reverse('prospectos:lista_prospectos_inactivo'))
        self.assertEqual(resp.status_code, 200)

    def test_view_prospectos_20_2(self):
        resp = self.client.get(reverse('prospectos:lista_prospectos'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['prospectos']), 20)


class ProspectoTest(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345', is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
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

    # ACCEPTANCE CRITERIA: 13.3
    def test_ac_13_3(self):
        resp = self.client.post(reverse('prospectos:crear_empresa'), {
            'Telefono': '4422232226',
            'email': 'correo@itesm.com',
            'razon_social': 'Escuela'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['Error'], 'Forma invalida, favor de revisar sus respuestas de nuevo')

    # Test Django
    def test_crear_prospecto(self):
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
        prospecto_acum = Prospecto.objects.filter(email='a01209537@itesm.mx').count()
        self.assertEqual(prospecto_acum, 1)

    def test_prospecto_mismo_mail(self):
        try:
            Prospecto.objects.get_or_create(
                nombre='Marco Antonio',
                apellidos='Luna Calvillo',
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
            prospecto_acum = Prospecto.objects.all().count()
            self.assertEqual(prospecto_acum, 0)
        except:
            prospecto_acum = Prospecto.objects.all().count()
            self.assertEqual(prospecto_acum, 1)

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
        prospecto = Prospecto.objects.create(
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
        resp = self.client.post(reverse('prospectos:editar_prospecto', kwargs={'pk': prospecto.id}),
                                {'nombre': 'Luis Alfredo', 'apellidos': 'Rodriguez Santos','telefono_casa':
                                    '4422232226', 'telefono_celular': '4422580662', 'direccion':
                                    Lugar.objects.get(calle='Lourdes'), 'email': 'a01209537@itesm.mx',
                                 'metodo_captacion': 'Facebook', 'estado_civil': 'SOLTERO', 'ocupacion': 'Estudiante',
                                 'hijos': 1}, follow=True)
        actualizado = Prospecto.objects.get(id=prospecto.id)
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(actualizado, 'Marco Antonio Luna Calvillo')

    # Acceptance Criteria 8.1
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
        p = Prospecto.objects.create(
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
        resp = self.client.post(reverse('prospectos:baja_prospecto', kwargs={'pk': p.id}), follow=True)
        actualizado = Prospecto.objects.get(id=p.id)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(actualizado.activo, False)


class ActividadTest(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345', is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        cls.lugar = Lugar.objects.create(
            calle='Paraiso',
            numero_interior='',
            numero_exterior='38',
            colonia='Satelite',
            estado='Queretaro',
            ciudad='Queretaro',
            pais='Mexico',
            codigo_postal='76125'
        )
        cls.prospecto = Prospecto.objects.create(
            nombre='Pablo',
            apellidos='Martinez Villareal',
            telefono_casa='4422232226',
            telefono_celular='4422580662',
            email='pmartinez@gmail.com',
            direccion=cls.lugar,
            metodo_captacion='Facebook',
            estado_civil='Soltero',
            ocupacion='Estudiante',
            hijos=1,
            activo=True,
        )
        cls.curso = Curso.objects.create(nombre='Mi Curso', descripcion='Este es el grupo de pruebas automoatizadas.')
        cls.grupo = Grupo.objects.create(nombre='Grupo', curso=cls.curso, fecha_inicio='2018-03-16',
                                         fecha_fin='2018-03-16', direccion='Calle', descripcion='Curso de marzo',
                                         costo=1000)
        cls.relacion = ProspectoGrupo.objects.create(prospecto=cls.prospecto, grupo=cls.grupo, interes='ALTO',
                                                     flag_cadhu=False)
        cls.act_false = Actividad.objects.create(titulo='Actividad False', fecha=datetime.datetime.now().date(),
                                                 notas='Llamada con el prosecto', prospecto_grupo=cls.relacion,
                                                 terminado=False)
        cls.act_true = Actividad.objects.create(titulo='Actividad True', fecha=datetime.datetime.now().date(),
                                                notas='Llamada con el prosecto', prospecto_grupo=cls.relacion,
                                                terminado=True)

    # ACCEPTANCE CRITERIA: 12.1
    def test_ac_12_1(self):
        resp = self.client.post(reverse('prospectos:crear_actividad', kwargs={'pk': self.relacion.id}), {
            'titulo': 'Llamada con el prospecto',
            'fecha': datetime.datetime.now().date(),
            'notas': 'Llamada con el prosecto',
            'prospecto_grupo': self.relacion})
        act_count = Actividad.objects.all().count()
        self.assertEqual(act_count, 3)

    # ACCEPTANCE CRITERIA: 12.2
    def test_ac_12_2(self):
        resp = self.client.post(reverse('prospectos:crear_actividad', kwargs={'pk': self.relacion.id}), {
            'titulo': 'Llamada con el prospecto',
            'fecha': False,
            'hora': 'Hora',
            'notas': 'Llamada con el prosecto'
        })
        mensaje = get_messages(resp)
        self.assertEqual(resp.context['Error'], 'Forma inválida')

    def test_ac_12_3(self):
        resp = self.client.post(reverse('prospectos:estado_actividad', kwargs={'pk': self.act_false.id}))
        self.assertEqual(self.act_false.terminado, False)

    def test_ac_12_4(self):
        self.client.post(reverse('prospectos:estado_actividad', kwargs={'pk': self.act_true.id}))
        self.assertEqual(self.act_true.terminado, True)


class CargaMasivaTest(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345', is_superuser=True)
        usuario1.save()
        self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        cls.lugar, cls.created = Lugar.objects.get_or_create(
            calle='Paraiso',
            numero_interior='',
            numero_exterior='38',
            colonia='Satelite',
            estado='Queretaro',
            ciudad='Queretaro',
            pais='Mexico',
            codigo_postal='76125'
        )
        cls.prospecto = Prospecto.objects.create(
            nombre='Alejandro',
            apellidos='Salmon FD',
            telefono_casa='4422232226',
            telefono_celular='4422580662',
            email='asalmon@cadhu.com',
            direccion=cls.lugar,
            metodo_captacion='Facebook',
            estado_civil='Soltero',
            ocupacion='Estudiante',
            hijos=1,
            activo=True,
        )
        cls.prospecto_2 = Prospecto.objects.create(
            nombre=' Pedro',
            apellidos='Salmon FD',
            telefono_casa='4422232226',
            telefono_celular='4422580662',
            email='prospecto2@cadhu.com',
            direccion=cls.lugar,
            metodo_captacion='Facebook',
            estado_civil='Soltero',
            ocupacion='Estudiante',
            hijos=1,
            activo=True,
        )
        cls.curso = Curso.objects.create(nombre='Mi Curso', descripcion='Este es el grupo de pruebas automoatizadas.')
        cls.grupo = Grupo.objects.create(nombre='CursoPrueba', curso=cls.curso, fecha_inicio='2018-03-16',
                                         fecha_fin='2018-03-16', direccion='Calle', descripcion='Curso de marzo',
                                         costo=1000)
        cls.relacion = ProspectoGrupo.objects.create(prospecto=cls.prospecto, grupo=cls.grupo, interes='ALTO',
                                                     flag_cadhu=False)

    # ACCEPTANCE CRITERIA: 43.1
    def test_ac_43_1(self):
        csv = 'Nombre,Apellidos,Email,Telefono casa,Telefono celular,Metodo captacion,Estado civil,Ocupacion,Hijos,' \
              'Recomendacion,Pais,Estado,Ciudad,Colonia,Calle,Numero exterior,Numero interior,Codigo postal,ID grupo' \
              '\n Alejandro,Salmon FD,mancha@cadhu.com,4422232226,4422580662,Facebook,Soltero,Estudiante,1,,Mexico,' \
              'Queretaro,Queretaro,Satelite,Paraiso,38,,76125,'+str(self.grupo.id)
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
        prospecto_2 = Prospecto.objects.get(email='prospecto2@cadhu.com')
        prospecto_count = Prospecto.objects.all().count()
        prospecto_rel = ProspectoGrupo.objects.filter(prospecto=prospecto).count()
        prospecto_2_rel = ProspectoGrupo.objects.filter(prospecto_id=prospecto_2.id).count()
        self.assertEqual(prospecto_count, 3)
        self.assertEqual(prospecto_rel, 1)
        self.assertEqual(prospecto_2_rel, 0)

    # ACCEPTANCE CRITERIA: 43.2
    def test_ac_43_2(self):
        grupo = Grupo.objects.get(nombre='CursoPrueba').id
        csv = 'Nombre,Apellidos,Email,Telefono casa,Telefono celular,Metodo captacion,Estado civil,Ocupacion,Hijos,' \
              'Recomendacion,Pais,Estado,Ciudad,Colonia,Calle,Numero exterior,Numero interior,Codigo postal,ID grupo' \
              '\n Pedro,Salmon FD,prospecto2@cadhu.com,4422232226,4422580662,Facebook,Soltero,' \
              'Estudiante,1,,Mexico,Queretaro,Queretaro,Satelite,Paraiso,38,,76125,'+str(grupo)
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
        prospecto_count = Prospecto.objects.all().count()
        prospecto_rel = ProspectoGrupo.objects.all().count()
        self.assertEqual(prospecto_count, 2)
        # self.assertEqual(prospecto_rel, 2)

    # ACCEPTANCE CRITERIA: 43.3
    def test_ac_43_3(self):
        grupo = Grupo.objects.get(nombre='CursoPrueba').id
        csv = 'Nombre,Apellidos,Email,Telefono casa,Telefono celular,Metodo captacion,Estado civil,Ocupacion,Hijos,' \
              'Recomendacion,Pais,Estado,Ciudad,Colonia,Calle,Numero exterior,Numero interior,Codigo postal,ID grupo' \
              '\n Alejandro,Salmon FD,asalmon@cadhu.com,4422232226,4422580662,Facebook,Soltero,Estudiante,1,,Mexico,' \
              'Queretaro,Queretaro,Satelite,Paraiso,38,,76125,'+str(grupo)
        prospecto = Prospecto.objects.get(email='asalmon@cadhu.com')
        prospecto_count_antes = Prospecto.objects.filter(id=prospecto.id).count()
        prospecto_rel_antes = ProspectoGrupo.objects.filter(prospecto=prospecto).count()
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
        prospecto_rel = ProspectoGrupo.objects.filter(prospecto=prospecto).count()
        self.assertEqual(prospecto_count, prospecto_count_antes)
        self.assertEqual(prospecto_rel, prospecto_rel_antes)

    # ACCEPTANCE CRITERIA: 43.4
    def test_ac_43_4(self):
        grupo = Grupo.objects.get(nombre='CursoPrueba').id
        csv = 'Nombre,Apellidos,Email,Telefono casa,Telefono celular,Metodo captacion,Estado civil,Ocupacion,Hijos,' \
              'Recomendacion,Pais,Estado,Ciudad,Colonia,Calle,Numero exterior,Numero interior,Codigo postal,ID grupo' \
              '\n Pedro,Salmon FD,asalmon@cadhu.com,1234567890,4422580662,Facebook,Soltero,Estudiante,1,,Mexico,' \
              'Queretaro,Queretaro,Satelite,Paraiso,38,,76125,'+str(grupo)
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
        grupo = Grupo.objects.get(nombre='CursoPrueba').id
        csv = 'Nombre,Apellidos,Email,Telefono casa,Telefono celular,Metodo captacion,Estado civil,Ocupacion,Hijos,' \
              'Recomendacion,Pais,Estado,Ciudad,Colonia,Calle,Numero exterior,Numero interior,Codigo postal,ID grupo' \
              '\n Alejandro,Salmon FD,prospecto2@cadhu.com,4422232226,4422580662,Facebook,Soltero,Estudiante,1,,' \
              'Mexico,Queretaro,Queretaro,Satelite,Paraiso,38,,76125,102'
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
        prospecto_rel = ProspectoGrupo.objects.filter(prospecto=prospecto).count()
        self.assertEqual(prospecto_count, 1)
        self.assertEqual(prospecto_rel, 0)


class VistaCursosTest(TestCase):
    def SetUP(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345', is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        cls.lugar = Lugar.objects.create(calle='Paraiso', numero_interior='', numero_exterior='38', colonia='Satelite',
                                         estado='Queretaro', ciudad='Queretaro', pais='Mexico', codigo_postal='76125')
        cls.prospecto = Prospecto.objects.create(nombre='Pablo', apellidos='Martinez Villareal',
                                                 telefono_casa='4422232226', telefono_celular='4422580662',
                                                 email='asdas@gmail.com', direccion=cls.lugar, ocupacion='Estudiante',
                                                 activo=True)
        cls.prospecto_2 = Prospecto.objects.create(nombre='Pablin', apellidos='Martinez Villareal',
                                                   telefono_casa='4422232226', telefono_celular='4422580662',
                                                   email='asdasin@gmail.com', direccion=cls.lugar, ocupacion='Estudiante',
                                                   activo=True)
        cls.curso = Curso.objects.create(nombre='Mi Curso', descripcion='Este es el grupo de pruebas automoatizadas.')
        cls.grupo = Grupo.objects.create(nombre='Grupo', curso=cls.curso, fecha_inicio='2018-03-16',
                                         fecha_fin='2018-03-16', direccion='Calle', descripcion='Curso de marzo',
                                         costo=1000)
        cls.prospecto_grupo = ProspectoGrupo.objects.create(fecha='2025-03-15', interes='ALTO', flag_cadhu=False,
                                                            status='INTERESADO', grupo=cls.grupo,
                                                            prospecto=cls.prospecto)
        cls.prospecto_grupo_2 = ProspectoGrupo.objects.create(fecha='2025-03-15', interes='ALTO', flag_cadhu=False,
                                                              status='INTERESADO', grupo=cls.grupo,
                                                              prospecto=cls.prospecto_2)
        cls.pago = Pago.objects.create(fecha='2018-03-15', monto=200, referencia="1651",
                                       prospecto_grupo=cls.prospecto_grupo, comentarios="comentario de prueba")
        cls.cliente = Cliente.objects.create(matricula='asd123', fecha='2018-03-15',
                                             prospecto_grupo=cls.prospecto_grupo)

    def testListaClientes(self):
        resp = self.client.post(reverse('prospectos:lista_clientes'),)
        clientes = Cliente.objects.filter(activo=True).order_by('fecha')
        self.assertEqual(1, clientes.count())


class PagoTest(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345', is_superuser=True)
        usuario1.save()
        self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        lugar = Lugar.objects.create(calle='Paraiso', numero_interior='', numero_exterior='38', colonia='Satelite',
                                     estado='Queretaro', ciudad='Queretaro', pais='Mexico', codigo_postal='76125' )
        prospecto = Prospecto.objects.create(nombre='Pablo', apellidos='Martinez Villareal', telefono_casa='4422232226',
                                             telefono_celular='4422580662', email='asdas@gmail.com', direccion=lugar,
                                             ocupacion='Estudiante', activo=True)
        curso = Curso.objects.create(nombre='Mi Curso', descripcion='Este es el grupo de pruebas automoatizadas.')
        grupo = Grupo.objects.create(nombre='Grupo', curso=curso, fecha_inicio='2018-03-16', fecha_fin='2018-03-16',
                                     direccion='Calle', descripcion='Curso de marzo', costo=1000)
        prospecto_grupo = ProspectoGrupo.objects.create(fecha='2025-03-15', interes='ALTO', flag_cadhu=False,
                                                        status='INTERESADO', grupo_id=grupo.id, prospecto=prospecto)
        pago = Pago.objects.create(fecha='2018-03-15', monto=200, referencia="1651", prospecto_grupo=prospecto_grupo,
                                   comentarios="comentario de prueba", tipo_pago="Efectivo")
        cliente = Cliente.objects.create(matricula='asd123', fecha='2018-03-15', prospecto_grupo=prospecto_grupo)

    def test_ac_42_1(self):
        id_pe = ProspectoGrupo.objects.get(fecha='2025-03-15').id
        resp = self.client.get(reverse('prospectos:lista_pagos', kwargs={'id_pe': id_pe}))
        self.assertEqual(resp.status_code, 200)

    def test_ac_41_2(self):
        id_pe = ProspectoGrupo.objects.get(fecha='2025-03-15').id
        resp = self.client.post(reverse('prospectos:nuevo_pago', kwargs={'id_pe': id_pe}), {
            "fecha": '2025-03-15',
            "monto": 200,
            "referencia": "1651",
            "prospecto_grupo_id": id_pe,
            "comentarios": "comentario de prueba",
            "tipo_pago": "Efectivo"
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
