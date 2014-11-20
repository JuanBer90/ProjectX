from django import forms
from django.forms.widgets import TextInput,NumberInput,FileInput
from AdminItems.models import Item, Document




class ItemForm(forms.ModelForm):
    
    nombre=forms.CharField(widget=TextInput(attrs={'class': 'form-control','required':'required'}),
                           max_length=40, help_text="Maximo 30 caracteres",label="Nombre")
    descripcion=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows':'3','required':'required'}),
                                help_text="Maximo 300 caracteres",max_length=300,label="Descripcion")
    prioridad=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','value':'0','max':'1000'}),
                                help_text="",min_value=0,label="Prioridad")
    costo=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','value':'0'}),
                                help_text="",min_value=0,label="Costo")
    complejidad=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','value':'0','max':'1000'}),
                                help_text="",min_value=0,label="Complejidad")
  #  fase=forms.IntegerField(label="Numero de fases",help_text="Maximo 10 fases",
   #                widget=forms.TextInput(attrs={'class': 'form-control','type':'number','min':'1','max':'10'}))
    class Meta:
        model = Item
        fields = ['nombre','descripcion','prioridad','costo','complejidad']
        

    def save(self, commit=True):
        objeto = super(ItemForm, self).save(commit=False)
        if commit:
            objeto.save()
        return objeto


class UploadFileForm(forms.Form):
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}),max_length=50)
    docfile = forms.FileField(widget=FileInput(attrs={'class':'form-control'}))
    
class DocumentForm(forms.Form):
    class Meta:
        model = Document
    docfile = forms.FileField(widget=FileInput(attrs={'class': 'form-control'}),
        label='Select a file',
        help_text='max. 42 megabytes'
    )
    nombre = forms.CharField(widget=TextInput(attrs={'class': 'form-control'}),max_length=50)
    