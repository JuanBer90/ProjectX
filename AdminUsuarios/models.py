from django import forms
from django.db import models


# Create your models here.
from bootstrap_toolkit import widgets

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User
from AdminProyectos.models import Proyecto


class Miembro(models.Model):
    """
    Modelo de Proyecto con su respectivo atributos
    """
    class Meta:
        db_table='miembros'
    proyecto=models.ForeignKey(Proyecto)
    usuario=models.ForeignKey(User)
    
    
