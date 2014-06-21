from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect

from demo_project.demo_app.models import Rol, Permisos, RolUser


def nuevo_rol(request, id_proyecto=0,id=0):
    """
        Crea el Rol con sus posibles permisos
    """
    user=request.user
    user_rol=RolUser.objects.filter(user_id=user.id)

    if user_rol.count() == 0 and not user.is_staff and not user.is_superuser:
          return HttpResponseRedirect('/sinpermiso/')

    # if not user_rol.rol.permisos.add_rol:
    #       return HttpResponseRedirect('/sinpermiso/')

    if id > 0:
        rol = Rol.objects.get(pk=id)
        permiso = Permisos.objects.get(pk=rol.permisos_id)
        modo = 'Editar'
    else:
        rol = Rol()
        permiso = Permisos()

        modo = 'Crear'

    if request.method=='POST':

        rol_name=request.POST.get('rol_name','')
        rol_descripcion=request.POST.get('rol_description','')

        aux_total = Rol.objects.filter(nombre=rol_name)
        existe = aux_total.count()
        if existe > 0  and modo == 'Crear':
            return render_to_response('HtmlRoles/nuevorol.html',{'rol_ya':True}, context_instance=RequestContext(request))
        permiso.AdminProyecto=request.POST.get('proyecto',False)
        permiso.AdminFase=request.POST.get('fase',False)
        permiso.AdminItem=request.POST.get('item',False)
        permiso.AdminRol=request.POST.get('rol',False)
        permiso.AdminUser=request.POST.get('user',False)
        permiso.save()
        rol.descripcion=rol_descripcion
        rol.permisos=permiso
        rol.nombre = rol_name
        rol.save()
        return HttpResponseRedirect('/roles/'+str(id_proyecto))

    return render_to_response('HtmlRoles/nuevorol.html',{'rol':rol,'permiso':permiso,'modo':modo}, context_instance=RequestContext(request))


def roles(request, id_proyecto):
    """
    Buscador de Roles
    """

    nro_lineas=10
    lines = []
    page = request.GET.get('page')
    if request.method=='POST':
        buscar=request.POST["buscar"]
    else:
        buscar = ''

    if buscar == '':
        proyectos_total = Rol.objects.count()
    else:
        permisos_list = Rol.objects.filter(nombre=buscar)
        proyectos_total = permisos_list.count()

    for i in range(proyectos_total):
        lines.append(u'Line %s' % (i + 1))
    paginator = Paginator(lines, nro_lineas)
    try:
        page=int(page)
    except:
        page=1

    if int(page)*nro_lineas>proyectos_total or int(page)>0:
        try:
            items = paginator.page(page)
            fin=int(page)*nro_lineas
            ini =fin-nro_lineas
        except PageNotAnInteger or EmptyPage:
            fin=nro_lineas
            ini=0
            items = paginator.page(1)
    else:
        fin=nro_lineas
        ini=0
        items = paginator.page(1)
    if buscar == '':
        proyectos_list = Rol.objects.order_by('nombre').all()[ini:fin]
    else:
        proyectos_list = Rol.objects.filter(nombre=buscar)[ini:fin]

    return render_to_response('HtmlRoles/roles.html',{'roles':proyectos_list,'id_proyecto':id_proyecto}, RequestContext(request, {
        'lines': items
    }))

def ver_rol(request,idRol,id_proyecto):
    rol=Rol.objects.get(id_rol=idRol)
    permiso=Permisos.objects.get(rol=rol.permisos_id)
    if request.method=='POST':
             return HttpResponseRedirect('/roles/'+str(id_proyecto))
    return render_to_response('HtmlRoles/verrol.html',{'rol':rol,'permiso':permiso,'modo':''}, context_instance=RequestContext(request))

def nuevo_rol_user(request,id_proyecto):
    user=request.user
    user_rol=RolUser.objects.filter(user_id=user.id)

    if user_rol.count() == 0 and not user.is_staff:
          return HttpResponseRedirect('/sinpermiso/')


    #if not user_rol.rol.permisos.asignar_rol:
    #      return HttpResponseRedirect('/sinpermiso/')

    # if not user_rol.rol.permisos.asignar_rol:
    #       return HttpResponseRedirect('/sinpermiso/')


    roles=Rol.objects.filter()
    users=User.objects.filter()
    msg=''
    if request.method=='POST':
       asignar=request.POST.get('button','Volver')
       if asignar == 'Volver':
           return HttpResponseRedirect('/proyecto/colaboradores/'+str(id_proyecto)+'/')
       id_rol=request.POST.get('rol_select',0)
       id_user=request.POST.get('user_select',0)
       if(id_rol > 0 and id_user > 0 ):
            aux=RolUser.objects.filter(proyecto_id=id_proyecto,user_id=id_user).count()
            if aux >0:
                msg='Este usuario ya posee un rol en este proyecto, desasignar rol primero'
                return render_to_response('HtmlRoles/asignarrol.html',{'users':users,'rol':roles, 'msg':msg}, context_instance=RequestContext(request))
            rol_user= RolUser()
            rol_user.rol_id = id_rol
            rol_user.user_id = id_user
            rol_user.proyecto_id=id_proyecto
            rol_user.save()
            return HttpResponseRedirect('/proyecto/colaboradores/'+str(id_proyecto)+'/')
       else:
            msg='Error..'

    return render_to_response('HtmlRoles/asignarrol.html',{'users':users,'rol':roles, 'msg':msg}, context_instance=RequestContext(request))

def sinpermiso(request):
    return render_to_response('HtmlUsuarios/sinpermiso.html')

def nuevo_leader(request):
     user=request.user
     if not user.is_superuser:
          return HttpResponseRedirect('/sinpermiso/')
     msg=''
     if request.method=='POST':
         id_user=request.POST.get('user_select',0)
         print 'id usuario: '+str(id_user)
         if id_user > 0:
             usuario=User.objects.get(pk=id_user)
             if usuario.is_staff:
                msg='El usuario "'+str(usuario.username)+'" ya es Leader'
             else:
                usuario.is_staff= True
                usuario.save()
     users=User.objects.all()
     return render_to_response('HtmlRoles/crearleader.html',{'users':users, 'msg':msg},context_instance=RequestContext(request))

def desasignar_rol(request,id_rol_user):
     rol_user=RolUser.objects.get(pk=id_rol_user)
     if request.method=='POST':
         delete=request.POST.get('delete','no')
         id_proyecto=rol_user.proyecto_id
         if delete == 'si':
             rol_user.delete()
         return HttpResponseRedirect('/proyecto/colaboradores/'+str(id_proyecto))
     return render_to_response('HtmlRoles/desasignar.html',{'r':rol_user},context_instance=RequestContext(request))
