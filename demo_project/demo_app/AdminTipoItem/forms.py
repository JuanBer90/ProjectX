from django import forms
from demo_project.demo_app.models import TipoItem
from django.forms.widgets import TextInput

class TipoItemForm(forms.ModelForm):

    nombre=forms.CharField(widget=TextInput, label="Nombre")
    descripcion=forms.CharField(widget=TextInput,label="Descripcion")

    class Meta:
        model = TipoItem
        fields = ['nombre','descripcion']
    def save(self, commit=True):
        tipoitem = super(TipoItemForm, self).save(commit=False)
        if commit:
           tipoitem.save()
        return tipoitem