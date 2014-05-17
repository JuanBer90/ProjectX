from django import forms
from demo_project.demo_app.models import AtributosPorItem
from demo_project.demo_app.models import Item
from django.forms.widgets import TextInput

class AtributosItemForm(forms.ModelForm):

    nombre=forms.CharField(widget=TextInput, label="Nombre")
    tipo=forms.CharField(widget=TextInput,label="Tipo")
    valor_defecto=forms.CharField(widget=TextInput,label="Valor Defecto")
    item=forms.forms.ModelChoiceField(queryset=Item.objects.all())

    class Meta:
        model = AtributosPorItem
        fields = ['nombre','tipo','Valor defecto','item']

    def save(self, commit=True):
        atributositem = super(AtributosItemForm, self).save(commit=False)
        if commit:
           atributositem.save()
        return atributositem