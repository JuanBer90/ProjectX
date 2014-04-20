from django import forms
from django.conf.app_template import models
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields.related import OneToOneField,ManyToOneRel
from django.forms.widgets import TextInput,PasswordInput,EmailInput, CheckboxChoiceInput
from django.forms.fields import CheckboxInput
from django.db import models
from demo_project.demo_app.AdminRoles.models import Rol

class RolForm(forms.ModelForm):
    nombre=forms.CharField(widget=TextInput,max_length=100, label="Nombre")
    descripcion= forms.Textarea(widget=TextInput,max_length=300,label="Descripcion")

    class Meta:
        model = Rol
        fields = ['nombre','descripcion']

    def save(self, commit=True):
        rol = super(RolForm, self).save(commit=False)
        if commit:
           rol.save()
        return rol
