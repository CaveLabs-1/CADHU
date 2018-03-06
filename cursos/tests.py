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
        #Set up non-modified objects used by all test methods
        evento = Evento.objects.create(Nombre='Mi Evento', Descripcion='Este es el evento de pruebas automoatizadas.')
        Curso.objects.create(Nombre='Curso', Evento= evento, Fecha='2018-03-16', Direccion='Calle', Descripcion='Evento de marzo', Costo=1000)

    def test_Nombre_label(self):
        curso=Curso.objects.get(id=1)
        field_label = curso._meta.get_field('Nombre').verbose_name
        self.assertEquals(field_label,'Nombre')

    def test_Evento_label(self):
        curso=Curso.objects.get(id=1)
        field_label = curso._meta.get_field('Evento').verbose_name
        self.assertEquals(field_label,'Evento')

    def test_Fecha_label(self):
        curso=Curso.objects.get(id=1)
        field_label = curso._meta.get_field('Fecha').verbose_name
        self.assertEquals(field_label,'Fecha')

    def test_Direccion_label(self):
        curso=Curso.objects.get(id=1)
        field_label = curso._meta.get_field('Direccion').verbose_name
        self.assertEquals(field_label,'Direccion')

    def test_Descripcion_label(self):
        curso=Curso.objects.get(id=1)
        field_label = curso._meta.get_field('Descripcion').verbose_name
        self.assertEquals(field_label,'Descripcion')

    def test_Costo_label(self):
        curso=Curso.objects.get(id=1)
        field_label = curso._meta.get_field('Costo').verbose_name
        self.assertEquals(field_label,'Costo')

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/cursos/nuevo_curso')
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get('/cursos/nuevo_curso')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'cursos/nuevo_curso.html')

# Create your tests here.
