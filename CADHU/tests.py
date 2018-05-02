from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from prospectos.models import Lugar, Actividad, Prospecto, ProspectoGrupo
from cursos.models import Curso
from grupos.models import Grupo
from django.contrib.auth.models import timezone


class NoAuthenticationViewTests(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345', is_superuser=True)
        usuario1.save()

    # Acceptance Criteria: 1.1
    def test_1_2(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, "/login/?next=/")


class AuthenticationViewTests(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345', is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

     #Acceptance Criteria: 1.1
    def test_1_1(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(str(response.context['user']), 'testuser1')

    # Acceptance Criteria: 2.1
    def test_2_1(self):
        response = self.client.get(reverse('prospectos:lista_prospectos'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.client.logout()
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, "/login/?next=/")


class PendientesViewTests(TestCase):
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
        cls.curso = Curso.objects.create(nombre='Mi Evento', descripcion='Este es el grupo de pruebas automoatizadas.')
        cls.grupo = Grupo.objects.create(nombre='GrupoPrueba', curso=cls.curso, fecha_inicio='2018-03-16', direccion='Calle',
                                         descripcion='Grupo de marzo', costo=1000)
        cls.relacion = ProspectoGrupo.objects.create(prospecto=cls.prospecto, grupo=cls.grupo, interes='ALTO',
                                                     flag_cadhu=False)

    def test_crear_actividad(self):
        resp = self.client.post(reverse('prospectos:crear_actividad', kwargs={'pk': self.relacion.pk}), {
            'titulo': 'Llamada con el prospecto',
            'tipo': 'SMS',
            'fecha': timezone.now().date(),
            'notas': 'Llamada con el prosecto',
            'prospecto_grupo': self.grupo})
        count = Actividad.objects.filter(prospecto_grupo=self.relacion)
        self.assertQuerysetEqual(count, ['<Actividad: Llamada con el prospecto>'])

    # Accepatnce criteria 20.1 - 20.2
    def test_mostrar_pendientes(self):
        resp = self.client.get(reverse('index'))
        self.assertEqual(resp.status_code, 200)
