from demo_project.demo_app.AdminProyectos.models import Proyecto
from django import forms

class proyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto