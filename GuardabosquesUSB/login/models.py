from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm

CARRERA_CHOICES = (
    (0, 'Arquitectura'),
    (1, 'Ing. Computacion'),
    (2, 'Ing. Electrica'),
    (3, 'Ing. Electronica'),
    (4, 'Ing. Geofisica'),
    (5, 'Ing. Mantenimiento'),
    (6, 'Ing. Materiales'),
    (7, 'Ing. Mecanica'),
    (8, 'Ing. Produccion'),
    (9, 'Ing. Telecomunicaciones'),
    (10, 'Ing. Quimica'),
    (11, 'Lic. Biologia'),
    (12, 'Lic. Comercio Exterior'),
    (13, 'Lic. Gestion de la Hospitalidad'),
    (14, 'Lic. Fisica'),
    (15, 'Lic. Matematica'),
    (16, 'Lic. Quimica'),
    (17, 'Urbanismo'),
    (18, 'Admin. Aduanera'),
    (19, 'Admin. Hotelera'),
    (20, 'Admin. Transporte'),
    (21, 'Admin. Turismo'),
    (22, 'Comercio Exterior (Carrera Corta)'),
    (23, 'Mantenimiento Aeronautica'),
    (24, 'Organizacion Empresarial'),
    (25, 'Tec. Electrica'),
    (26, 'Tec. Electronica'),
    (27, 'Tec. Mecanica'),
)

class Estudiante(models.Model):
  user    = models.OneToOneField(User)
  carrera = models.IntegerField('carrera', choices=CARRERA_CHOICES, default=1)
  carnet  = models.CharField(max_length=8, default="")
  
class EstudianteForm(ModelForm):
  class Meta:
    model = Estudiante
    fields = ['carrera', 'carnet']
