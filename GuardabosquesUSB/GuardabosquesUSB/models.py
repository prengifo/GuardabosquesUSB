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

    HORAS_VALUES= (
        ('1',1),
        ('2',2),
        ('3',3),
        ('4',4),
        ('5',5),
        ('6',6),
        ('7',7),
        ('8',8),
        ('9',9),
        ('10',10),
        ('11',11),
        ('12',12),
    )

    horas        = models.PositiveIntegerField(choices=HORAS_VALUES)
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
