from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.db import models
from login.models import Estudiante
from datetime import datetime


class TipoActividad(models.Model):
    nombre = models.CharField(max_length = 200)

    def __unicode__(self):
        return self.nombre

class TipoActividadForm(ModelForm):
    class Meta:
        model = TipoActividad
        fields = ['nombre']

class Actividad(models.Model):

    ACTIVIDAD_CHOICES= (
        ('TV', 'Trabajo en vivero'),
        ('TC', 'Trabajo en campo'),
        ('JR', 'Jornada de reforestacion'),
        ('ER', 'Ecorrutas'),

    )

    HORAS_CHOICES= (
        (0, 'Esperando validacion'),
        (1, 'Horas Validadas'),
        (2, 'Horas  Rechazadas'),

    )

    horas        = models.PositiveIntegerField()
    descripcion  = models.ForeignKey(TipoActividad)
    validado_nuevo     = models.IntegerField(default=0,choices=HORAS_CHOICES)
    estudiante   = models.ForeignKey('login.Estudiante')
    fecha        = models.DateTimeField(default=datetime.now())

class ActividadForm(ModelForm):
    class Meta:
        model = Actividad
        fields = ['horas', 'descripcion', 'fecha']

class ValidacionForm(ModelForm):
    class Meta:
        model = Actividad
        fields =  []
