from django import forms
from django.conf.app_template import models
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields.related import OneToOneField,ManyToOneRel
from django.forms.widgets import TextInput,PasswordInput,EmailInput, CheckboxChoiceInput
from django.forms.fields import CheckboxInput
from django.db import models

class TipoContenidoForm(forms.ModelForm):
    name=forms.CharField(widget=TextInput,max_length=100, label="Nombre de Contenido")
    app_label= forms.CharField(widget=TextInput,max_length=100,label="Etiqueta")
    model=forms.CharField(widget=TextInput,max_length=100,label="Modelo")

    class Meta:
        model = ContentType
        fields = ['name','app_label','model']

    def save(self, commit=True):
        tipo_contenido = super(TipoContenidoForm, self).save(commit=False)
        if commit:
           tipo_contenido.save()
        return tipo_contenido


class PermisoForm(forms.ModelForm):
    name=forms.CharField(widget=TextInput,max_length=100, label="Nombre del permiso")
    codename=forms.CharField(widget=TextInput,max_length=100,label="Codigo de permiso")
    content_type = models.OneToOneField(Permission, primary_key=True)

    class Meta:
        model = Permission
        fields = ['name','codename','content_type']

    def save(self, commit=True):
        permiso = super(PermisoForm, self).save(commit=False)
        if commit:
           permiso.save()
        return permiso
