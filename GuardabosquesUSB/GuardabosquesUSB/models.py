from django.db import models
from django import forms
from django.contrib.auth.models import User


class Persona(models.Model):

  carnet     = models.CharField(max_length=8)
  nmb        = models.OneToOneField(User)
  carrera    = models.CharField(max_length=100)
  horas_completadas = models.IntegerField(default=0)

  def __unicode__(self):
      return self.carnet
