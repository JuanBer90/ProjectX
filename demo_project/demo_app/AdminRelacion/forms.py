from django import forms
from demo_project.demo_app.models import Relacion
from demo_project.demo_app.models import Item
from django.forms.widgets import TextInput

class RelacionForm(forms.ModelForm):

    tipo=forms.CharField(widget=TextInput, label="Tipo")
    codigo=forms.CharField(widget=TextInput,label="Codigo")
    anterior=forms.ModelChoiceField(queryset=Item.objects.all())
    posterior=forms.ModelChoiceField(queryset=Item.objects.all())


    class Meta:
        model = Relacion
        fields = ['tipo','codigo','anterior','posterior']

    def save(self, commit=True):
        relacion = super(RelacionForm, self).save(commit=False)
        if commit:
           relacion.save()
        return relacion

