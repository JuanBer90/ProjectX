from django import forms
from models import User
from django.contrib.contenttypes.models import ContentType
from django.forms.widgets import TextInput,PasswordInput,EmailInput, CheckboxChoiceInput
from django.forms.fields import CheckboxInput

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



class EditTipoContenidoForm(forms.ModelForm):
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