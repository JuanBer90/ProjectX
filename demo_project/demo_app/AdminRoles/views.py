from django.contrib.auth.models import User,ContentType, Permission
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from demo_project.demo_app.AdminPermisos.forms import TipoContenidoForm, PermisoForm
from demo_project.demo_app.AdminRoles.forms import RolUserForm, RolPermisoForm
from demo_project.demo_app.models import Rol
from demo_project.demo_app.models import RolPermiso


def nuevo_rol(request):
    if request.method=='POST':

        rol_name=request.POST.get('rol_name','')
        rol_descripcion=request.POST.get('rol_description','')

        aux_total = Rol.objects.filter(nombre=rol_name)
        existe = aux_total.count()
        if existe > 0 :
            return render_to_response('HtmlRoles/nuevorol.html',{'rol_ya':True}, context_instance=RequestContext(request))

        rol=Rol()
        rol.descripcion=rol_descripcion
        rol.nombre=rol_name
        rol.save()
        rol_saved=Rol.objects.filter(nombre=rol.nombre)[0]
        print 'a ver que pasa aca'+rol_saved.descripcion
        add_proyecto=request.POST.get('add_proyecto',False)
        edit_proyecto=request.POST.get('edit_proyecto',False)
        delete_proyecto=request.POST.get('delete_proyecto',False)
        add_fase=request.POST.get('add_fase',False)
        edit_fase=request.POST.get('edit_fase', False)
        delete_fase=request.POST.get('delte_fase', False)
        add_item=request.POST.get('add_item',False)
        edit_item=request.POST.get('edit_item', False)
        delete_item=request.POST.get('delete_item',False)
        revive_item=request.POST.get('revive_item',False)
        add_rol=request.POST.get('add_rol',False)
        edit_rol=request.POST.get('edit_rol',False)
        delete_rol=request.POST.get('delete_rol',False)

        if add_proyecto:
            permiso=Permission.objects.get(codename='add_proyecto')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol_saved
            rol_permiso.save()
        
        if edit_proyecto:
            permiso=Permission.objects.get(codename='edit_proyecto')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol_saved
            rol_permiso.save()

        if delete_proyecto:
            permiso=Permission.objects.get(codename='delete_proyecto')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol_saved
            rol_permiso.save()

        if add_fase:
            permiso=Permission.objects.get(codename='add_fase')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol_saved
            rol_permiso.save()

        if edit_fase:
            permiso=Permission.objects.get(codename='edit_fase')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol_saved
            rol_permiso.save()

        if delete_fase:
            permiso=Permission.objects.get(codename='delete_fase')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol_saved
            rol_permiso.save()

        if add_item:
            permiso=Permission.objects.get(codename='add_item')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol_saved
            rol_permiso.save()

        if edit_item:
            permiso=Permission.objects.get(codename='edit_item')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol_saved
            rol_permiso.save()

        if delete_item:
            permiso=Permission.objects.get(codename='delete_item')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol_saved
            rol_permiso.save()

        if revive_item:
            permiso=Permission.objects.get(codename='revive_item')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol_saved
            rol_permiso.save()

        if add_rol:
            permiso=Permission.objects.get(codename='add_rol')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol_saved
            rol_permiso.save()

        if edit_rol:
            permiso=Permission.objects.get(codename='edit_rol')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol_saved
            rol_permiso.save()

        if delete_rol:
            permiso=Permission.objects.get(codename='delete_rol')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol_saved
            rol_permiso.save()

        return HttpResponseRedirect('/roles/')


    return render_to_response('HtmlRoles/nuevorol.html',{}, context_instance=RequestContext(request))

# def roles(request):
#     nro_lineas=10
#     lines = []
#     page = request.GET.get('page')
#     roles_total = Rol.objects.count()
#     for i in range(roles_total):
#         lines.append(u'Line %s' % (i + 1))
#     paginator = Paginator(lines, nro_lineas)
#     try:
#         page=int(page)
#     except:
#         page=1
#
#     if int(page)*nro_lineas>roles_total or int(page)>0:
#         try:
#             users = paginator.page(page)
#             fin=int(page)*nro_lineas
#             ini =fin-nro_lineas
#         except PageNotAnInteger or EmptyPage:
#             fin=nro_lineas
#             ini=0
#             users = paginator.page(1)
#     else:
#         fin=nro_lineas
#         ini=0
#         users = paginator.page(1)
#     roles_list = Rol.objects.order_by('nombre').all()[ini:fin]
#
#     return render_to_response('HtmlRoles/roles.html',{'roles':roles_list,}, RequestContext(request, {
#         'lines': users
#     }))

def roles(request):
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

    return render_to_response('HtmlRoles/roles.html',{'roles':proyectos_list}, RequestContext(request, {
        'lines': items
    }))

def editar_rol(request,idRol):

    rol=Rol.objects.get(id_rol=idRol)
    permisos_rol=RolPermiso.objects.filter(rol=rol)
    codenames=[]
    for p in permisos_rol:
        codenames.append(p.permiso.codename)

    if request.method=='POST':
        rol_name=request.POST.get('rol_name','')
        aux_total = Rol.objects.filter(nombre=rol_name)
        existe = aux_total.count()
        if existe > 1 :
            return render_to_response('HtmlRoles/editarrol.html',{'rol':rol,'codenames':codenames,'rol_ya':True}, context_instance=RequestContext(request))
        rol_descripcion=request.POST.get('rol_description','')
        rol.descripcion=rol_descripcion
        rol.nombre=rol_name
        rol.save()

        add_proyecto=request.POST.get('add_proyecto',False)
        edit_proyecto=request.POST.get('edit_proyecto',False)
        delete_proyecto=request.POST.get('delete_proyecto',False)
        add_fase=request.POST.get('add_fase',False)
        edit_fase=request.POST.get('edit_fase', False)
        delete_fase=request.POST.get('delete_fase', False)
        add_item=request.POST.get('add_item',False)
        edit_item=request.POST.get('edit_item', False)
        delete_item=request.POST.get('delete_item',False)
        revive_item=request.POST.get('revive_item',False)
        add_rol=request.POST.get('add_rol',False)
        edit_rol=request.POST.get('edit_rol',False)
        delete_rol=request.POST.get('delete_rol',False)

        a='add_proyecto' in codenames
        if add_proyecto and not a :
            permiso=Permission.objects.get(codename='add_proyecto')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()
        elif not add_proyecto and a:
            permiso=Permission.objects.get(codename='add_proyecto')
            rol_permiso=RolPermiso.objects.get(rol=rol,permiso=permiso)
            rol_permiso.delete()


        a='edit_proyecto' in codenames
        if edit_proyecto and not a :
            permiso=Permission.objects.get(codename='edit_proyecto')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()
        elif not edit_proyecto and a:
            permiso=Permission.objects.get(codename='edit_proyecto')
            rol_permiso=RolPermiso.objects.get(rol=rol,permiso=permiso)
            rol_permiso.delete()

        a='delete_proyecto' in codenames
        if delete_proyecto and not a :
            permiso=Permission.objects.get(codename='delete_proyecto')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()
        elif not delete_proyecto and a:
            permiso=Permission.objects.get(codename='delete_proyecto')
            rol_permiso=RolPermiso.objects.get(rol=rol,permiso=permiso)
            rol_permiso.delete()

        a='add_fase' in codenames
        if add_fase and not a :
            permiso=Permission.objects.get(codename='add_fase')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()
        elif not add_fase and a:
            permiso=Permission.objects.get(codename='add_fase')
            rol_permiso=RolPermiso.objects.get(rol=rol,permiso=permiso)
            rol_permiso.delete()

        a='edit_fase' in codenames
        if edit_fase and not a :
            permiso=Permission.objects.get(codename='edit_fase')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()
        elif not edit_fase and a:
            permiso=Permission.objects.get(codename='edit_fase')
            rol_permiso=RolPermiso.objects.get(rol=rol,permiso=permiso)
            rol_permiso.delete()

        a='delete_fase' in codenames
        if delete_fase and not a :
            permiso=Permission.objects.get(codename='delete_fase')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()
        elif not delete_fase and a:
            permiso=Permission.objects.get(codename='delete_fase')
            rol_permiso=RolPermiso.objects.get(rol=rol,permiso=permiso)
            rol_permiso.delete()

        a='add_item' in codenames
        if add_item and not a :
            permiso=Permission.objects.get(codename='add_item')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()
        elif not add_item and a:
            permiso=Permission.objects.get(codename='add_item')
            rol_permiso=RolPermiso.objects.get(rol=rol,permiso=permiso)
            rol_permiso.delete()

        a='edit_item' in codenames
        if edit_item and not a :
            permiso=Permission.objects.get(codename='edit_item')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()
        elif not edit_item and a:
            permiso=Permission.objects.get(codename='edit_item')
            rol_permiso=RolPermiso.objects.get(rol=rol,permiso=permiso)
            rol_permiso.delete()

        a='delete_item' in codenames
        if delete_item and not a :
            permiso=Permission.objects.get(codename='delete_item')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()
        elif not delete_item and a:
            permiso=Permission.objects.get(codename='delete_item')
            rol_permiso=RolPermiso.objects.get(rol=rol,permiso=permiso)
            rol_permiso.delete()

        a='revive_item' in codenames
        if revive_item and not a :
            permiso=Permission.objects.get(codename='revive_item')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()
        elif not revive_item and a:
            permiso=Permission.objects.get(codename='revive_item')
            rol_permiso=RolPermiso.objects.get(rol=rol,permiso=permiso)
            rol_permiso.delete()

        a='add_rol' in codenames
        if add_rol and not a :
            permiso=Permission.objects.get(codename='add_rol')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()
        elif not add_rol and a:
            permiso=Permission.objects.get(codename='add_rol')
            rol_permiso=RolPermiso.objects.get(rol=rol,permiso=permiso)
            rol_permiso.delete()

        a='edit_rol' in codenames
        if edit_rol and not a :
            permiso=Permission.objects.get(codename='edit_rol')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()
        elif not edit_rol and a:
            permiso=Permission.objects.get(codename='edit_rol')
            rol_permiso=RolPermiso.objects.get(rol=rol,permiso=permiso)
            rol_permiso.delete()

        a='delete_rol' in codenames
        if delete_rol and not a :
            permiso=Permission.objects.get(codename='delete_rol')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()
        elif not delete_rol and a:
            permiso=Permission.objects.get(codename='edit_rol')
            rol_permiso=RolPermiso.objects.get(rol=rol,permiso=permiso)
            rol_permiso.delete()

        return HttpResponseRedirect('/roles/')


    return render_to_response('HtmlRoles/editarrol.html',{'rol':rol,'codenames':codenames}, context_instance=RequestContext(request))


def eliminar_rol(request, idRol):
    rol= Rol.objects.get(pk=idRol)
    if request.method=='POST':
        delete= request.POST['delete']
        if delete == 'si':
             permisos_rol=RolPermiso.objects.filter(rol=rol)
             for p in permisos_rol:
                p.delete()
             rol.delete()

        return HttpResponseRedirect('/roles/')

    return render_to_response('HtmlRoles/eliminarrol.html',{'rol':rol},
                              context_instance=RequestContext(request))




def ver_rol(request,idRol):

    rol=Rol.objects.get(id_rol=idRol)
    permisos_rol=RolPermiso.objects.filter(rol=rol)
    codenames=[]
    for p in permisos_rol:
        codenames.append(p.permiso.codename)

    return render_to_response('HtmlRoles/verrol.html',{'rol':rol,'codenames':codenames}, context_instance=RequestContext(request))

    
def nuevo_rol_user(request):
    if request.method=='POST':
        formulario= RolUserForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/roles/')
    else:
        formulario= RolUserForm(request.POST)
    return render_to_response('HtmlRoles/nuevoroluser.html',{'formulario':formulario}, context_instance=RequestContext(request))


def nuevo_rol_permiso(request):
    if request.method=='POST':
        formulario= RolPermisoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/roles/')
    else:
        formulario= RolPermisoForm(request.POST)
    return render_to_response('HtmlRoles/nuevoroluser.html',{'formulario':formulario}, context_instance=RequestContext(request))