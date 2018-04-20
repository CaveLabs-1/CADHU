from django.test import TestCase
from grupos.models import Grupo
from cursos.models import Curso
from prospectos.models import Lugar, Prospecto, ProspectoGrupo
from django.urls import reverse
from django.contrib.auth.models import User, Group
# Create your tests here.


class CursoModelTest(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345', is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.curso = Curso.objects.create(nombre='Mi grupo', descripcion='Este es el grupo de pruebas automoatizadas.')
        cls.curso = Grupo.objects.create(nombre='Grupo', curso=cls.curso, fecha_inicio='2018-03-16', fecha_fin='2018-03-20',
                                         direccion='Calle', descripcion='Grupo de marzo', costo=1000)

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('grupos:nuevo_grupo'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('grupos:nuevo_grupo'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'grupos/form_grupo.html')

    def test_view_urlgrupos_exists_at_desired_location(self):
        resp = self.client.get(reverse('grupos:grupos'))
        self.assertEqual(resp.status_code, 200)

    def test_view_crear_grupo(self):
        curso = Curso.objects.create(nombre='Mi Curso 2', descripcion='Este es el grupo de pruebas automoatizadas.')
        resp = self.client.post('/grupos/nuevo_grupo',  {
            'nombre': 'Grupo',
            'grupo': curso,
            'fecha_inicio': '2018-03-16',
            'fecha_fin': '2018-03-16',
            'direccion': 'Calle',
            'descripcion': 'Curso de marzo',
            'costo': 1000},
            follow=True
        )
        self.assertEqual(resp.status_code, 200)


class CursoViewTest(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        cls.curso = Curso.objects.create(nombre='Mi Curso', descripcion='Este es el grupo de pruebas automoatizadas.')
        Grupo.objects.create(nombre='Grupo', curso=cls.curso, fecha_inicio='2018-03-16', fecha_fin='2018-03-16',
                             direccion='Calle', descripcion='Curso de marzo', costo=1000)

    # Acceptance criteria: 29.1
    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('grupos:grupos'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'grupos/grupos.html')

    # Acceptance criteria: 29.2
    def test_view_grupo_existe(self):
        resp = self.client.get(reverse('grupos:grupos'))
        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(resp.context['grupos'], ['<Grupo: Grupo>'])


class BorrarGrupoTest(TestCase):
    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        cls.lugar = Lugar.objects.create(calle='Paraiso', numero_interior='', numero_exterior='38', colonia='Satelite',
                                         estado='Queretaro', ciudad='Queretaro', pais='Mexico', codigo_postal='76125')
        cls.curso = Curso.objects.create(nombre='Curso 1', descripcion='Curso para desactivar')
        cls.grupo1 = Grupo.objects.create(nombre='Grupo 1', curso=cls.curso, fecha_inicio='2018-03-16',
                                          fecha_fin='2018-03-16', direccion='Calle', descripcion='Curso de marzo', costo=1000)
        cls.grupo2 = Grupo.objects.create(nombre='Grupo 2', curso=cls.curso, fecha_inicio='2018-03-16',
                                          fecha_fin='2018-03-16', direccion='Calle', descripcion='Curso de marzo', costo=1000)
        cls.prospecto = Prospecto.objects.create(nombre='Pablo', apellidos='Martinez Villareal',
                                                 telefono_casa='4422232226', telefono_celular='4422580662', email='asdas@gmail.com',
                                                 direccion=cls.lugar, ocupacion='Estudiante', activo=True)
        cls.prospecto_grupo = ProspectoGrupo.objects.create(fecha='2025-03-15', interes='ALTO', flag_cadhu=False,
                                                            status='INTERESADO', grupo=cls.grupo1, prospecto=cls.prospecto)

    def test_ac_28_1(self):
        resp = self.client.get(reverse('grupos:eliminar_grupo', kwargs={'pk': self.grupo2.id}))
        deleted_group = Grupo.objects.filter(nombre="Grupo 2").count()
        self.assertEqual(deleted_group, 0)

    def test_ac_28_2(self):
        resp = self.client.get(reverse('grupos:eliminar_grupo', kwargs={'pk': self.grupo1.id}))
        grupo_actualizado = Grupo.objects.get(pk=self.grupo1.id)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(grupo_actualizado.activo, False)
