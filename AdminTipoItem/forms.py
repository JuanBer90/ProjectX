from django import forms
from django.forms.widgets import TextInput
from AdminTipoItem.models import TipoItem



class TipoItemForm(forms.ModelForm):
    
    nombre=forms.CharField(widget=TextInput(attrs={'class': 'form-control','required':'required'}),
                           max_length=30, help_text="Maximo 30 caracteres",label="Nombre")
    descripcion=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows':'3','required':'required'}),
                                help_text="Maximo 300 caracteres",max_length=300,label="Descripcion")
  #  fase=forms.IntegerField(label="Numero de fases",help_text="Maximo 10 fases",
   #                widget=forms.TextInput(attrs={'class': 'form-control','type':'number','min':'1','max':'10'}))
    class Meta:
        model = TipoItem
        fields = ['nombre','descripcion']
        

    def save(self, commit=True):
        objeto = super(TipoItemForm, self).save(commit=False)
        if commit:
            objeto.save()
        return objeto

