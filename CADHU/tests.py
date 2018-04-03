from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group, Lugar, Actividad

class NoAuthenticationViewTests(TestCase):

    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()

    #Acceptance Criteria: 1.1
    def test_1_2(self):
        response = self.client.get(reverse('index:index'))
        self.assertRedirects(response, reverse('index:index'))


class AuthenticationViewTests(TestCase):

    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    #Acceptance Criteria: 1.1
    def test_1_1(self):
        response = self.client.get(reverse('index:index'))
        self.assertEqual(str(response.context['user']), 'testuser1')

    #Acceptance Criteria: 2.1
    def test_2_1(self):
        response = self.client.get(reverse('prospectos:lista_prospectos'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.client.logout()
        response = self.client.get(reverse('index:index'))
        self.assertRedirects(response, reverse('index:index'))

class PendientesViewTests(TestCase):
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

    def test_crear_actividad(self):
        resp = self.client.post(reverse('prospectos:crear_actividad',kwargs={'id':1}),{
            'titulo':'Llamada con el prospecto',
            'fecha':datetime.datetime.now().date(),
            'notas':'Llamada con el prosecto',
            'prospecto_evento':1})
        self.assertQuerysetEqual(resp.context['actividades'],['<Actividad: Llamada con el prospecto>'])

    # Accepatnce criteria 20.1 - 20.2
    def test_mostrar_pendientes(self):
        resp = self.client.get(reverse('index: index'))
        self.assertEqual(resp.status_code, 200)
