from django.db import models
from django import forms

class Persona(models.Model):

  nombre     = models.CharField(max_length=100)
  apellido   = models.CharField(max_length=100)
  carnet     = models.CharField(max_length=8, primary_key=True
  email      = models.CharField(max_length=100)
  carrera    = models.CharField(max_length=100)
  clave =    = models.CharField(widget=PasswordInput())

  def __unicode__(self):
      return self.nombre+' '+self.apellido
