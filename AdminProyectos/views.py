 # coding=UTF-8
from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from AdminProyectos.forms import ProyectoForm, ProyectoFormEdit
from AdminFases.models import Fase
from AdminProyectos.models import Proyecto
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required



def nuevo_proyecto(request):
    """
    Crea un nuevo proyecto
    """
    user=request.user
    #if not user.is_staff:
     #   return HttpResponseRedirect('/sinpermiso')
    if request.method=='POST':
        formulario= ProyectoForm(request.POST)
        if formulario.is_valid():
            proyecto= formulario.save()
            proyecto.leader = request.user
            proyecto.estado='NOI'
            proyecto.coste_total=0
            proyecto.fecha_creacion = today()
            proyecto.save()
            messages.success(request, 'PROYECTO CREADO CON EXITO!')
        
                        

            #aux = Rol.objects.filter(nombre='Leader').count()
            #===================================================================
            # if aux == 0:
            #    rol= crearRolLeader()
            # else:
            #     rol = Rol.objects.get(nombre='Leader')
            # rol_user=RolUser()
            # rol_user.rol = rol
            # rol_user.proyecto = proyecto
            # rol_user.user = user
            # rol_user.save()
            #===================================================================
            return HttpResponseRedirect('/proyecto/miproyecto/'+str(proyecto.id))
    else:
        formulario= ProyectoForm(request.POST)
    return render_to_response('HtmlProyecto/nuevoproyecto.html',{'formulario':formulario,'user':user},
                              context_instance=RequestContext(request))

#===============================================================================
# def crearRolLeader():
#     permiso=Permisos()
#     permiso.AdminFase=True
#     permiso.AdminItem=True
#     permiso.AdminRol=True
#     permiso.AdminProyecto=True
#     permiso.AdminUser=True
#     permiso.save()
#     rol=Rol()
#     rol.nombre='Leader'
#     rol.permisos=permiso
#     rol.descripcion='Este rol tiene permiso absoluto sobre un proyecto'
#     rol.save()
#     return rol
#===============================================================================

def iniciar_proyecto(request, id_proyecto):
    proyecto= Proyecto.objects.get(pk=id_proyecto)
    proyecto.estado='INI'
    proyecto.save()
    messages.success(request,'Proyecto "'+proyecto.nombre+'" iniciado')
    for i in range(0,proyecto.nro_fases):
        fase=Fase()
        fase.numero=i+1
        fase.proyecto = proyecto
        fase.save() 
    return HttpResponseRedirect('/proyecto/miproyecto/'+str(id_proyecto))

def editar_proyecto(request, id_proyecto):
 
    proyecto= Proyecto.objects.get(pk=id_proyecto)
    user=request.user
    #get_roles=RolUser.objects.filter(user=user,proyecto=proyecto)
 #==============================================================================
 #    if get_roles.count() == 0:
 #        return HttpResponseRedirect('/sinpermiso')
 #    for r in get_roles:
 #        if not r.rol.permisos.AdminProyecto:
 #            return HttpResponseRedirect('/sinpermiso')
 # 
 #==============================================================================
    if request.method=='POST':
        formulario= ProyectoFormEdit(request.POST,instance=proyecto)
        if formulario.is_valid():
            proyecto= formulario.save()
            proyecto.save()
            return HttpResponseRedirect('/proyecto/miproyecto/'+str(id_proyecto))
    else:
        formulario= ProyectoFormEdit(instance=proyecto)
    return render_to_response('HtmlProyecto/editarproyecto.html',
                {'formulario':formulario,'id_proyecto':id_proyecto,'user':proyecto.leader},
                              context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def proyectos(request):
    buscar=''
    if request.method == 'GET':
        buscar=request.GET.get('buscar','')
    objetos_list = Proyecto.objects.filter(nombre__icontains=buscar)
    paginator = Paginator(objetos_list, 10) # Show 25 contacts per page

    page = request.GET.get('page','')
    try:
        page=int(page)
    except:
        page=1    
    try:
        objetos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objetos = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objetos = paginator.page(paginator.num_pages)

    return render_to_response('HtmlProyecto/proyectos.html',
                {'objetos':objetos,'page_range':paginator.page_range,
                 'page':int(page),'buscar':buscar,'placeholder':'Proyecto','total':objetos_list.count()
                                                                }, RequestContext(request))



def eliminar_proyecto(request, id_proyecto):
    proyecto= Proyecto.objects.get(pk=id_proyecto)
    user=request.user
 #==============================================================================
 #    #get_roles=RolUser.objects.filter(user=user,proyecto=proyecto)
 #    if get_roles.count() == 0:
 #        return HttpResponseRedirect('/sinpermiso')
 # 
 #    for r in get_roles:
 #        if not r.rol.permisos.delete_project:
 #            return HttpResponseRedirect('/sinpermiso')
 # 
 #==============================================================================
    nombre=proyecto.nombre
    proyecto.delete()
    
    messages.success(request,"Proyecto "+nombre+" Eliminado!")
    return HttpResponseRedirect('/proyectos/')

 
    return render_to_response('HtmlProyecto/eliminarproyecto.html',{'proyecto':proyecto},
                              context_instance=RequestContext(request))
def mis_proyectos(request):
    #query= "select p.nombre, p.id_proyecto from proyectos p right join rol_user r on r.proyecto_id = p.id_proyecto where r.user_id ="+str(request.user.id)
    proyectos_list=Proyecto.objects.all()
    #proyectos_list=execute_query(query)
    
    #proyectos_list= Proyecto.objects.raw(query)
    return render_to_response('HtmlProyecto/misproyectos.html',{'proyectos':proyectos_list})


def mi_proyecto(request, id_proyecto):
 
    proyecto= Proyecto.objects.get(pk=id_proyecto)
    user=request.user
    #get_roles=RolUser.objects.filter(user=user,proyecto=proyecto)
    #===========================================================================
    # if get_roles.count() == 0:
    #     return HttpResponseRedirect('/sinpermiso')
    # for r in get_roles:
    #     if not r.rol.permisos.AdminProyecto:
    #         return HttpResponseRedirect('/sinpermiso')
    #===========================================================================
    if request.method=='POST':
        formulario= ProyectoForm(request.POST,instance=proyecto)
        if formulario.is_valid():
            proyecto= formulario.save()
            proyecto.save()
            return HttpResponseRedirect('/proyecto/miproyecto/'+str(id_proyecto))
    else:
        formulario= ProyectoForm(instance=proyecto)

    return render_to_response('HtmlProyecto/miproyecto.html',
                {'formulario':formulario,'proyecto':proyecto,
                 'id_proyecto':id_proyecto,'user':proyecto.leader},
                              context_instance=RequestContext(request))

def colaboradores(request, id_proyecto):
    #===========================================================================
    # rol_user=RolUser.objects.filter(proyecto_id=id_proyecto).exclude(user_id=request.user.id)
    # roles=RolUser.objects.all()
    #===========================================================================
    return render_to_response('HtmlProyecto/colaboradores.html',
                              {'roles_user':'',#rol_user,
                               'id_proyecto':id_proyecto, 'roles':'',#roles
                               })
