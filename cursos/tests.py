from django.test import TestCase
from cursos.models import Curso
from eventos.models import Evento
from prospectos.models import Lugar, Prospecto, ProspectoEvento
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

class BorrarGrupoTest(TestCase):

    def setUp(self):
        Group.objects.create(name="administrador")
        Group.objects.create(name="vendedora")
        usuario1 = User.objects.create_user(username='testuser1', password='12345',is_superuser=True)
        usuario1.save()
        login = self.client.login(username='testuser1', password='12345')

    @classmethod
    def setUpTestData(cls):
        lugar = Lugar.objects.create( Calle='Paraiso', Numero_Interior='', Numero_Exterior='38', Colonia='Satelite', Estado='Queretaro', Ciudad='Queretaro', Pais='Mexico', Codigo_Postal='76125' )
        curso = Evento.objects.create(Nombre='Evento 1', Descripcion='Evento para desactivar')
        grupo1 = Curso.objects.create(Nombre='Grupo 1', Evento= curso, Fecha_Inicio='2018-03-16', Fecha_Fin='2018-03-16', Direccion='Calle', Descripcion='Evento de marzo', Costo=1000)
        grupo2 = Curso.objects.create(Nombre='Grupo 2', Evento= curso, Fecha_Inicio='2018-03-16', Fecha_Fin='2018-03-16', Direccion='Calle', Descripcion='Evento de marzo', Costo=1000)
        prospecto = Prospecto.objects.create( Nombre='Pablo', Apellidos='Martinez Villareal', Telefono_Casa='4422232226', Telefono_Celular='4422580662', Email='asdas@gmail.com', Direccion= lugar, Ocupacion='Estudiante', Activo=True)
        prospecto_evento = ProspectoEvento.objects.create(Fecha='2025-03-15', Interes='ALTO', FlagCADHU=False, status='INTERESADO', Curso_id= grupo1.id, Prospecto_id = prospecto.id)

    def test_ac_28_1(self):
        grupo = Curso.objects.get(Nombre="Grupo 2")
        resp = self.client.get(reverse('cursos:eliminar_grupo', kwargs={'id': grupo.id}))
        deleted_group = Curso.objects.filter(Nombre="Grupo 2").count()
        self.assertEqual(deleted_group, 0)

    def test_ac_28_2(self):
        grupo = Curso.objects.get(Nombre="Grupo 1")
        resp = self.client.get(reverse('cursos:eliminar_grupo', kwargs={'id': grupo.id}))
        grupo_actualizado = Curso.objects.get(id=grupo.id)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(grupo_actualizado.Activo, False)
