from django.http.response import HttpResponseRedirect
from demo_project.demo_app.models import Permisos, Rol


def create_rol(request):
    aux=Rol.objects.filter(nombre='Leader').count()
    if aux !=0:
        return HttpResponseRedirect('/')
    permiso=Permisos()
    permiso.AdminProyecto=True
    permiso.AdminUser=True
    permiso.AdminRol=True
    permiso.AdminFase=True
    permiso.AdminItem=True
    permiso.save()
    rol=Rol()
    rol.permisos=permiso
    rol.nombre='Leader'
    rol.descripcion='Este rol tiene permiso absoluto sobre el proyecto'
    rol.save()
    return HttpResponseRedirect('/')
