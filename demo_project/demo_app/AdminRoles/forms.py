from django import forms
# from django.conf.app_template import models
# from django.contrib.auth.models import Permission, User
# from django.contrib.contenttypes.models import ContentType
from django.db.models.fields.related import OneToOneField,ManyToOneRel
from django.contrib.auth.models import User, Permission
from django.forms.widgets import TextInput,Textarea
# from django.forms.fields import CheckboxInput
# from django.db import models
# from demo_project.demo_app.AdminRoles.models import Rol
#
# class RolForm(forms.ModelForm):
#     nombre=forms.CharField(widget=TextInput,max_length=100, label="Nombre")
#     descripcion= forms.CharField(widget=Textarea(attrs={'rows':'3' }),max_length=300,label="Descripcion")
#
#     class Meta:
#         model = Rol
#         fields = ['nombre','descripcion']
#
#     def save(self, commit=True):
#         rol = super(RolForm, self).save(commit=False)
#         if commit:
#            rol.save()
#         return rol
from demo_project.demo_app.models import Rol, RolUser, RolPermiso
from django.db import models



class RolUserForm(forms.ModelForm):
    #rol=forms.ModelChoiceField(queryset=Rol.objects.all())
    rol=forms.ModelChoiceField(queryset=Rol.objects.all())
    user=forms.ModelChoiceField(queryset=User.objects.all())
    #rol = models.OneToOneField(Rol)
    #user = models.OneToOneField(User)

    class Meta:
        model=RolUser
        fields = ['rol','user']


    def save(self, commit=True):
        rol_user = super(RolUserForm, self).save(commit=False)
        if commit:
           rol_user.save()
        return rol_user

class RolPermisoForm(forms.ModelForm):
    rol = forms.ModelChoiceField(queryset=Rol.objects.all().order_by('nombre'))
    permiso = forms.ModelChoiceField(queryset=Permission.objects.all())
    class Meta:
        model = RolPermiso

    def save(self, commit=True):
        rol_user = super(RolPermisoForm, self).save(commit=False)
        if commit:
           rol_user.save()
        return rol_user

