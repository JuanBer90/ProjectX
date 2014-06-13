from gufw import model
from django import forms
from demo_project.demo_app.models import TipoItem, Item
from django.forms.widgets import TextInput
from django import forms

class ItemForm(forms.ModelForm):
    nombre=forms.CharField(widget=TextInput,max_length=30, label="nombre")
    descripcion=forms.CharField(widget=TextInput,label="numero")
    numero=forms.IntegerField(label='Numero')
    numero_por_tipo=forms.IntegerField(label='Nro por Tipo')
    tipo_item=forms.IntegerField(label='Tipo de Item')
    fase=forms.ComboField(label='fase')

    class Meta:
        model = Item
        fields = ['nombre','numero','numero_por_tipo','tipo_item','fase']

    def save(self, commit=True):
        objeto = super(ItemForm, self).save(commit=False)
        if commit:
           objeto.save()
        return objeto



class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )


