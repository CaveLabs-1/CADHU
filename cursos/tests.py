from django.test import TestCase
from cursos.models import Curso
from eventos.models import Evento
from django.urls import reverse
from django.contrib.auth.models import User, Group
# Create your tests here.

class CursoModelTest(TestCase):

    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        evento = Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')
        curso = Curso.objects.create(Nombre='Curso', Evento= evento, Fecha_Inicio='2018-03-16', Fecha_Fin='2018-03-20', Direccion='Calle', Descripcion='Evento de marzo', Costo=1000)

    def test_Nombre_label(self):

        curso=Curso.objects.get(Nombre='Curso')
        field_label = curso._meta.get_field('Nombre').verbose_name
        self.assertEquals(field_label,'Nombre')

    def test_Evento_label(self):
        curso=Curso.objects.get(Nombre='Curso')
        field_label = curso._meta.get_field('Evento').verbose_name
        self.assertEquals(field_label,'Evento')

    def test_Fecha_Inicio_label(self):
        curso=Curso.objects.get(Nombre='Curso')
        field_label = curso._meta.get_field('Fecha_Inicio').verbose_name
        self.assertEquals(field_label,'Fecha Inicio')

    def test_Fecha_Fin_label(self):
        curso=Curso.objects.get(Nombre='Curso')
        field_label = curso._meta.get_field('Fecha_Fin').verbose_name
        self.assertEquals(field_label,'Fecha Fin')

    def test_Direccion_label(self):
        curso=Curso.objects.get(Nombre='Curso')
        field_label = curso._meta.get_field('Direccion').verbose_name
        self.assertEquals(field_label,'Direccion')

    def test_Descripcion_label(self):
        curso=Curso.objects.get(Nombre='Curso')
        field_label = curso._meta.get_field('Descripcion').verbose_name
        self.assertEquals(field_label,'Descripcion')

    def test_Costo_label(self):
        curso=Curso.objects.get(Nombre='Curso')
        field_label = curso._meta.get_field('Costo').verbose_name
        self.assertEquals(field_label,'Costo')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('cursos:nuevo_curso'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('cursos:nuevo_curso'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cursos/nuevo_curso.html')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get(reverse('cursos:cursos'))
        self.assertEqual(resp.status_code, 200)

    def test_view_crear_curso(self):
        evento = Evento.objects.create(Nombre='Mi Evento 2', Descripcion='Este es el evento de pruebas automoatizadas.')
        resp = self.client.post('/cursos/nuevo_curso',  {
            'Nombre': 'Curso',
            'Evento': evento,
            'Fecha_Inicio': '2018-03-16',
            'Fecha_Fin': '2018-03-16',
            'Direccion': 'Calle',
            'Descripcion': 'Evento de marzo',
            'Costo': 1000},
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
        evento = Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')
        Curso.objects.create(Nombre='Curso', Evento= evento, Fecha_Inicio='2018-03-16', Fecha_Fin='2018-03-16', Direccion='Calle', Descripcion='Evento de marzo', Costo=1000)

    #Acceptance criteria: 29.1
    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('cursos:cursos'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cursos/cursos.html')

    #Acceptance criteria: 29.2
    def test_view_curso_existe(self):
        resp = self.client.get(reverse('cursos:cursos'))
        self.assertEqual(resp.status_code, 200)
        self.assertQuerysetEqual(resp.context['cursos'],['<Curso: Curso>'])

# Create your tests here.
