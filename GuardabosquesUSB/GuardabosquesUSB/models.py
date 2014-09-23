from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.db import models
from login.models import Estudiante
from datetime import datetime   

class Actividad(models.Model):

    ACTIVIDAD_CHOICES= (
        ('TV', 'Trabajo en vivero'),
        ('TC', 'Trabajo en campo'),
        ('JR', 'Jornada de reforestacion'),
        ('ER', 'Ecorrutas'),

    )

    horas        = models.IntegerField()
    descripcion  = models.CharField(max_length=200, choices=ACTIVIDAD_CHOICES)
    validado     = models.BooleanField(default=False)
    estudiante   = models.ForeignKey('login.Estudiante')
    fecha        = models.DateTimeField(default=datetime.now())

class ActividadForm(ModelForm):
    class Meta:
        model = Actividad
        fields = ['horas', 'descripcion', 'fecha']

class ValidacionForm(ModelForm):
    class Meta:
        model = Actividad
        fields = ['id', 'estudiante', 'horas', 'descripcion', 'fecha', 'validado']
        widgets = {
           'estudiante': forms.HiddenInput(),
           'id' : forms.HiddenInput(),
        }

    # def clean_estudiante(self):
    #     print "FUI LLAMADO"
    #     estudiante = self.cleaned_data['estudiante']
    #     if estudiante is None:
    #         return self.fields['estudiante'].initial
    #     return estudiante
