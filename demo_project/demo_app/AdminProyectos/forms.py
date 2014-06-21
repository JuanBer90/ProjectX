from django import forms
from django.core.context_processors import request
from django.http import request
from demo_project.demo_app.models import Proyecto
from django.contrib.auth.models import User
from django.forms.widgets import TextInput
from django.db import models



class ProyectoForm(forms.ModelForm):
    """
    Atributos que el usuario deber completar para la creacion
    de un nuevo proyecto
    """

    #leader=forms.CharField(widget=TextInput(attrs={'readonly':'readonly'}),required=False)
    nombre=forms.CharField(widget=TextInput,max_length=30, label="Nombre del Proyecto")
    descripcion=forms.CharField(widget=forms.Textarea,max_length=300,label="Descripcion")
    #leader=forms.ModelChoiceField(queryset=User.objects.all())
    #fecha_creacion=forms.DateTimeField()
    # complejidad=forms.IntegerField(label="Complejidad")
    nro_fases=forms.IntegerField(label="Numero de fases")
    #estado=forms.BooleanField(label="Estado")
    #coste_total=forms.IntegerField(label="Coste Total")

    class Meta:
        model = Proyecto
        fields = ['nombre','descripcion','nro_fases']

    def save(self, commit=True):
        proyecto = super(ProyectoForm, self).save(commit=False)
        # if commit:
        #    proyecto.save()
        return proyecto



class ProyectoFormEdit(forms.ModelForm):
    """
    Atributos que el usuario deber completar para la creacion
    de un nuevo proyecto
    """

    #leader=forms.CharField(widget=TextInput(attrs={'readonly':'readonly'}),required=False)
    nombre=forms.CharField(widget=TextInput,max_length=30, label="Nombre del Proyecto")
    descripcion=forms.CharField(widget=forms.Textarea,max_length=300,label="Descripcion")
    #leader=forms.ModelChoiceField(queryset=User.objects.all())
    #fecha_creacion=forms.DateTimeField()
    # complejidad=forms.IntegerField(label="Complejidad")

    #estado=forms.BooleanField(label="Estado")
    #coste_total=forms.IntegerField(label="Coste Total")

    class Meta:
        model = Proyecto
        fields = ['nombre','descripcion']

    def save(self, commit=True):
        proyecto = super(ProyectoFormEdit, self).save(commit=False)
        # if commit:
        #    proyecto.save()
        return proyecto
