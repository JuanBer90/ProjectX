from django.contrib.auth.models import User,ContentType, Permission
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from demo_project.demo_app.AdminPermisos.forms import TipoContenidoForm, PermisoForm
from demo_project.demo_app.models import Rol
from demo_project.demo_app.models import RolPermiso


def nuevo_rol(request):
    if request.method=='POST':

        rol_name=request.POST.get('rol_name','')
        rol_descripcion=request.POST.get('rol_description','')
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

#         return HttpResponseRedirect('/roles/')


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
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()




        if edit_proyecto:
            permiso=Permission.objects.get(codename='edit_proyecto')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()

        if delete_proyecto:
            permiso=Permission.objects.get(codename='delete_proyecto')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()

        if add_fase:
            permiso=Permission.objects.get(codename='add_fase')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()

        if edit_fase:
            permiso=Permission.objects.get(codename='edit_fase')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()

        if delete_fase:
            permiso=Permission.objects.get(codename='delete_fase')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()

        if add_item:
            permiso=Permission.objects.get(codename='add_item')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()

        if edit_item:
            permiso=Permission.objects.get(codename='edit_item')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()

        if delete_item:
            permiso=Permission.objects.get(codename='delete_item')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()

        if revive_item:
            permiso=Permission.objects.get(codename='revive_item')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()

        if add_rol:
            permiso=Permission.objects.get(codename='add_rol')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()

        if edit_rol:
            permiso=Permission.objects.get(codename='edit_rol')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()

        if delete_rol:
            permiso=Permission.objects.get(codename='delete_rol')
            rol_permiso=RolPermiso()
            rol_permiso.permiso=permiso
            rol_permiso.rol=rol
            rol_permiso.save()
        return HttpResponseRedirect('/roles/')


    return render_to_response('HtmlRoles/editarrol.html',{'rol':rol,'codenames':codenames}, context_instance=RequestContext(request))
