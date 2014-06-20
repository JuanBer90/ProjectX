from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from demo_project.demo_app import constantes
from demo_project.demo_app.AdminProyectos.forms import ProyectoForm
from demo_project.demo_app.constantes import EstadoProyecto, execute_query
from demo_project.demo_app.models import Proyecto, RolUser, Rol, Fase, Permisos


def nuevo_proyecto(request):
    """
    Crea un nuevo proyecto
    """
    user=request.user
    if not user.is_staff:
        return HttpResponseRedirect('/sinpermiso')
    if request.method=='POST':
        formulario= ProyectoForm(request.POST)
        if formulario.is_valid():
            proyecto= formulario.save()
            proyecto.leader = request.user
            proyecto.estado=True
            proyecto.coste_total=0
            proyecto.fecha_creacion = today()
            proyecto.save()
            for i in range(0,proyecto.nro_fases):
                fase=Fase()
                fase.numero=i+1
                fase.proyecto = proyecto
                fase.save()

            aux = Rol.objects.filter(nombre='Leader').count()
            if aux == 0:
               rol= crearRolLeader()
            else:
                rol = Rol.objects.get(nombre='Leader')
            rol_user=RolUser()
            rol_user.rol = rol
            rol_user.proyecto = proyecto
            rol_user.user = user
            rol_user.save()
            return HttpResponseRedirect('/proyecto/miproyecto/'+str(proyecto.id_proyecto))
    else:
        formulario= ProyectoForm(request.POST)
    return render_to_response('HtmlProyecto/nuevoproyecto.html',{'formulario':formulario,'user':user},
                              context_instance=RequestContext(request))

def crearRolLeader():
    permiso=Permisos()
    permiso.AdminFase=True
    permiso.AdminItem=True
    permiso.AdminRol=True
    permiso.AdminProyecto=True
    permiso.AdminUser=True
    permiso.save()
    rol=Rol()
    rol.nombre='Leader'
    rol.permisos=permiso
    rol.descripcion='Este rol tiene permiso absoluto sobre un proyecto'
    rol.save()
    return rol
def editar_proyecto(request, id_proyecto):

    proyecto= Proyecto.objects.get(pk=id_proyecto)
    user=request.user
    get_roles=RolUser.objects.filter(user=user,proyecto=proyecto)
    if get_roles.count() == 0:
        return HttpResponseRedirect('/sinpermiso')
    for r in get_roles:
        if not r.rol.permisos.AdminProyecto:
            return HttpResponseRedirect('/sinpermiso')

    if request.method=='POST':
        formulario= ProyectoForm(request.POST,instance=proyecto)
        if formulario.is_valid():
            proyecto= formulario.save()
            proyecto.save()
            return HttpResponseRedirect('/proyectos')
    else:
        formulario= ProyectoForm(instance=proyecto)
    return render_to_response('HtmlProyecto/editarproyecto.html',{'formulario':formulario,'id_proyecto':id_proyecto,'user':proyecto.leader},
                              context_instance=RequestContext(request))



def proyectos(request):

    user=request.user
    if not user.is_staff and not user.is_superuser:
        return HttpResponseRedirect('/sinpermiso')

    nro_lineas=10
    lines = []
    page = request.GET.get('page')
    proyectos_total = Proyecto.objects.count()
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


    proyectos_list = Proyecto.objects.order_by('nombre').all()[ini:fin]

    return render_to_response('HtmlProyecto/proyectos.html',{'proyectos':proyectos_list}, RequestContext(request, {
        'lines': items
    }))

def eliminar_proyecto(request, id_proyecto):
    proyecto= Proyecto.objects.get(pk=id_proyecto)
    user=request.user
    get_roles=RolUser.objects.filter(user=user,proyecto=proyecto)
    if get_roles.count() == 0:
        return HttpResponseRedirect('/sinpermiso')

    for r in get_roles:
        if not r.rol.permisos.delete_project:
            return HttpResponseRedirect('/sinpermiso')

    if request.method=='POST':
        delete= request.POST['delete']
        if delete == 'si':
            proyecto.delete()

        return HttpResponseRedirect('/proyectos/')


    return render_to_response('HtmlProyecto/eliminarproyecto.html',{'proyecto':proyecto},
                              context_instance=RequestContext(request))
def mis_proyectos(request):
    query= "select p.nombre, p.id_proyecto from proyectos p right join rol_user r on r.proyecto_id = p.id_proyecto where r.user_id ="+str(request.user.id)
    proyectos_list=execute_query(query)
    print query
    #proyectos_list= Proyecto.objects.raw(query)
    for p in proyectos_list:
        print p
    print proyectos_list
    return render_to_response('HtmlProyecto/misproyectos.html',{'proyectos':proyectos_list})



def mi_proyecto(request, id_proyecto):

    proyecto= Proyecto.objects.get(pk=id_proyecto)
    user=request.user
    get_roles=RolUser.objects.filter(user=user,proyecto=proyecto)
    if get_roles.count() == 0:
        return HttpResponseRedirect('/sinpermiso')
    for r in get_roles:
        if not r.rol.permisos.AdminProyecto:
            return HttpResponseRedirect('/sinpermiso')

    if request.method=='POST':
        proyecto.estado=EstadoProyecto().PRO_IN
        proyecto.save()
        #
        # formulario= ProyectoForm(request.POST,instance=proyecto)
        # if formulario.is_valid():
        #     proyecto= formulario.save()
        #     proyecto.save()
        #     return HttpResponseRedirect('/proyectos')
    else:
        formulario= ProyectoForm(instance=proyecto)
    return render_to_response('HtmlProyecto/miproyecto.html',{'formulario':formulario,'proyecto':proyecto,'id_proyecto':id_proyecto,'user':proyecto.leader},
                              context_instance=RequestContext(request))

def colaboradores(request, id_proyecto):
    rol_user=RolUser.objects.filter(proyecto_id=id_proyecto).exclude(user_id=request.user.id)
    roles=RolUser.objects.all()
    return render_to_response('HtmlProyecto/colaboradores.html',{'roles_user':rol_user,'id_proyecto':id_proyecto, 'roles':roles})