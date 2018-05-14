from django.db import models
from grupos.models import Grupo
from django.utils import timezone
from cursos.models import Curso
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
# Create your models here.

METODO_CAPTACION = (
    ('Facebook', 'Facebook'),
    ('Buscador', 'Buscador'),
    ('Sitio Web', 'Sitio Web'),
    ('Email', 'Email'),
    ('Triptico/Cartel', 'Triptico/Cartel'),
    ('Radio', 'Radio'),
    ('Recomendacion', 'Recomendacion'),
    ('Otro', 'Otro'),
)

ESTATUS = (
    ('INTERESADO', 'INTERESADO'),
    ('CURSANDO', 'CURSANDO'),
    ('FINALIZADO', 'FINALIZADO'),
)

TIPOS_INTERES = (
    ('BAJO', 'BAJO'),
    ('MEDIO', 'MEDIO'),
    ('ALTO', 'ALTO'),
    ('MUY ALTO', 'MUY ALTO'),
    # ('PAGADO', 'PAGADO'),
)

ESTADO_CIVIL = (
    ('SOLTERO', 'SOLTERO'),
    ('CASADO', 'CASADO'),
    ('DIVORCIADO', 'DIVORCIADO'),
    ('UNION LIBRE', 'UNION LIBRE'),
)

TIPO_PAGO = (
    ('EFECTIVO', 'EFECTIVO'),
    ('CHEQUES', 'CHEQUES'),
    ('CLIP', 'CLIP'),
    ('DEPOSITO BANCARIO', 'DEPOSITO BANCARIO'),
    ('DEPOSITO OXXO', 'DEPOSITO OXXO'),
    ('PAYPAL', 'PAYPAL'),
    ('TARJETA DE CRÉDITO', 'TARJETA DE CRÉDITO'),
    ('TARJETA DE DÉBITO', 'TARJETA DE DÉBITO'),
    ('TRASFERENCIA ELECTRÓNICA', 'TRANSFERENCIA ELECTRÓNICA'),
)

ACTIVO = (
    (True, 'Activo'),
    (False, 'Inactivo'),
)

TIPO_ACTIVIDAD = (
    ('WHATSAPP', 'WHATSAPP'),
    ('E-MAIL', 'E-MAIL'),
    ('LLAMADA', 'LLAMADA'),
    ('SMS', 'SMS'),
)


class Lugar(models.Model):
    calle = models.CharField(max_length=50, blank=True, null=True)
    numero_interior = models.CharField(max_length=6, blank=True, null=True)
    numero_exterior = models.CharField(max_length=6, blank=True, null=True)
    colonia = models.CharField(max_length=50, blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    pais = models.CharField(max_length=50, blank=True, null=True, )
    codigo_postal = models.CharField(max_length=5, blank=True, null=True)


class Prospecto(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False)
    apellidos = models.CharField(max_length=120, blank=False, null=False)
    telefono_casa = models.CharField(max_length=15, blank=True, null=True)
    telefono_celular = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=False, null=False, unique=True)
    direccion = models.ForeignKey(Lugar, on_delete=models.SET_NULL, null=True, blank=True)
    metodo_captacion = models.CharField(max_length=50, blank=True, null=True, choices=METODO_CAPTACION)
    estado_civil = models.CharField(max_length=15, blank=True, null=True, choices=ESTADO_CIVIL)
    ocupacion = models.CharField(max_length=15, blank=True, null=True)
    hijos = models.PositiveIntegerField(blank=True, null=True, default=0)
    recomendacion = models.CharField(max_length=150, blank=True, null=True)
    grupos = models.ManyToManyField(Grupo, through='ProspectoGrupo', through_fields=('prospecto', 'grupo'))
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    fecha_creacion = models.DateField(null=True)
    activo = models.BooleanField(default=True, blank=True, choices=ACTIVO)
    empresa = models.ForeignKey('Empresa', null=True, on_delete=models.SET_NULL, blank=True)
    comentarios = models.CharField(max_length=3000, blank=True, null=True)

    def __str__(self):
        return self.nombre + ' ' + self.apellidos


class ProspectoGrupo(models.Model):
    prospecto = models.ForeignKey(Prospecto, on_delete=models.CASCADE, null=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, null=True)
    fecha = models.DateField(null=True, blank=True)
    interes = models.CharField(max_length=50, blank=True, null=True, choices=TIPOS_INTERES)
    flag_cadhu = models.NullBooleanField(default=False, null=True, verbose_name='Bandera de interes')
    status = models.CharField(max_length=50, choices=ESTATUS, default='INTERESADO')

    def __str__(self):
        return str(self.id)

    def bitacora(self):
        return Actividad.objects.filter(prospecto_grupo=self.id, terminado=True).order_by('fecha').reverse()

    def agenda(self):
        return Actividad.objects.filter(prospecto_grupo=self.id, terminado=False).order_by('fecha')


class Cliente(models.Model):
    prospecto_grupo = models.ForeignKey(ProspectoGrupo, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=12, unique=True, blank=False, null=False)
    fecha = models.DateField(null=True, blank=True, default=timezone.now().date())
    rfc_regex = RegexValidator(regex=r'^([A-ZÑ&]{3,4}) ?(?:- ?)?(\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])) ?(?:- ?)?([A-Z\d]{2})([A\d])$',
                               message="El RFC debe de contar con el formato oficial")
    rfc = models.CharField(validators=[rfc_regex], max_length=13, blank=True, null=True)
    direccion_facturacion = models.ForeignKey('Lugar', on_delete=models.SET_NULL, blank=True, null=True)
    razon_social = models.CharField(max_length=50, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.matricula


class Actividad(models.Model):
    titulo = models.CharField(verbose_name='Actividad', max_length=500)
    fecha = models.DateField(verbose_name='Fecha de la actividad', blank=False, null=False)
    hora = models.TimeField(verbose_name='Hora de la actividad', blank=True, null=True)
    notas = models.CharField(verbose_name='Notas de la actividad', max_length=4000, blank=True, null=True)
    prospecto_grupo = models.ForeignKey(ProspectoGrupo, on_delete=models.CASCADE)
    terminado = models.BooleanField(default=False, verbose_name='Terminada')
    tipo = models.CharField(null=True, blank=True, max_length=20, choices=TIPO_ACTIVIDAD,
                            verbose_name='Tipo de activdad.')

    def __str__(self):
        return self.titulo


class Pago(models.Model):
    # cliente
    prospecto_grupo = models.ForeignKey(ProspectoGrupo, on_delete=models.CASCADE)
    fecha = models.DateField(blank=True, null=True)
    monto = models.IntegerField(blank=True, null=True)
    referencia = models.CharField(max_length=50, blank=True, null=True, unique=True)
    validado = models.BooleanField(blank=False, default=False)
    comentarios = models.CharField(max_length=300, blank=True, null=True)
    tipo_pago = models.CharField(choices=TIPO_PAGO, max_length=50, blank=True, null=True)


class Empresa(models.Model):
    nombre = models.CharField(max_length=50, blank=False, null=False, unique=True)
    contacto_1 = models.CharField(max_length=50, blank=True, null=False)
    contacto_2 = models.CharField(max_length=50, blank=True, null=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="El telefono debe de contar con el siguiente formato: "
                                                               "'999999999'. Se permiten de 9 a 15 digitos.")
    telefono_1 = models.CharField(validators=[phone_regex], max_length=12, blank=True, null=True)
    telefono_2 = models.CharField(validators=[phone_regex], max_length=12, blank=True, null=True)
    email_1 = models.EmailField(max_length=50, blank=True, null=False)
    email_2 = models.EmailField(max_length=50, blank=True, null=False)
    puesto_1 = models.CharField(max_length=50, blank=True, null=False)
    puesto_2 = models.CharField(max_length=50, blank=True, null=False)
    direccion = models.ForeignKey(Lugar, on_delete=models.SET_NULL, null=True)
    razon_social = models.CharField(max_length=50, blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre
