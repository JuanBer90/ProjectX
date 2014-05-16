from django import forms
from models import User
from django.forms.widgets import TextInput,PasswordInput,EmailInput, CheckboxChoiceInput
from django.forms.fields import CheckboxInput


class RegistrationForm(forms.ModelForm):

    username=forms.CharField(widget=TextInput, label="username")
    first_name= forms.CharField(widget=TextInput,label="Nombre")
    last_name=forms.CharField(widget=TextInput,label="Apellido")
    email = forms.EmailField(widget=EmailInput,label="Email")
    password1 = forms.CharField(widget=PasswordInput,
                                label="Password")
    password2 = forms.CharField(widget=PasswordInput,
                                label="Password (again)")

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords no coinciden. Intentelo de nuevo.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
           user.save()
        return user



class EditUserForm(forms.ModelForm):
    username=forms.CharField(widget=TextInput(attrs={'readonly':'readonly'}), label="username")
    first_name= forms.CharField(widget=TextInput,label="Nombre")
    last_name=forms.CharField(widget=TextInput,label="Apellido")
    email = forms.EmailField(widget=EmailInput,label="Email")
    is_active = forms.BooleanField(required=False, label='Activo')
    is_staff = forms.BooleanField(required=False, label='Is Staff')


    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','is_active','is_staff']

    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)
        if commit:
           user.save()
        return user