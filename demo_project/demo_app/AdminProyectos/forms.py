from django import forms
from demo_project.demo_app.models import Proyecto
from django.contrib.auth.models import User
from django.forms.widgets import TextInput
from django.db import models



class ProyectoForm(forms.ModelForm):
    nombre=forms.CharField(widget=TextInput,max_length=30, label="Nombre del Proyecto")
    descripcion=forms.CharField(widget=TextInput,max_length=300,label="Descripcion")
    #complejidad=forms.IntegerField(label="Complejidad")
    #leader=models.OneToOneField(User)
    #nro_fases=forms.IntegerField(label="Numero de fases")
    #estado=forms.BooleanField(label="Estado")
    #coste_total=forms.IntegerField(label="Coste Total")

    class Meta:
        model = Proyecto
        fields = ['nombre','descripcion']
        #fields = ['nombre','descripcion','complejidad','leader','nro_fases','estado','estado','coste']

    def save(self, commit=True):
        proyecto = super(ProyectoForm, self).save(commit=False)
        if commit:
           proyecto.save()
        return proyecto

