from django import forms
from AdminAtributos.models import Atributo, TIPO_CHOICES
from django.forms.widgets import TextInput, ChoiceInput, DateInput, TimeInput

class AtributoForm(forms.ModelForm):
    class Meta:
        model=Atributo
        exclude=['fecha_creacion','tipo_item']
        widgets = { "fecha": forms.DateInput(attrs={'class': 'datepicker form-control','required':'required','type':'date'}),}
    
    nombre=forms.CharField(widget=TextInput(attrs={'class': 'form-control','required':'required'}),
                           max_length=40, help_text="Maximo 40 caracteres",label="Nombre")
    descripcion=forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control','rows':'3','required':'required'}),
                                help_text="Maximo 100 caracteres",max_length=100,label="Descripcion")
    tipo=forms.ChoiceField(choices=TIPO_CHOICES,widget=forms.Select(attrs={'class':'form-control','onchange':'select_tipo(this)','onclick':'alert(this)'}))
    cadena=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                help_text="Maximo 100 caracteres",max_length=200)
    numerico=forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control','max':'999999999','min':'-999999999','style':'text-align: right'}),)
    
    
   #fecha = forms.DateField(widget=DateInput(attrs={'class':'form-control'}))
    
    def save(self, commit=True):
        objeto = super(AtributoForm, self).save(commit)
        if commit:
            objeto.save()
        return objeto
    
