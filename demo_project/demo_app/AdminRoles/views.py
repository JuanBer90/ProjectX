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

def roles(request):
    nro_lineas=10
    lines = []
    page = request.GET.get('page')
    roles_total = Rol.objects.count()
    for i in range(roles_total):
        lines.append(u'Line %s' % (i + 1))
    paginator = Paginator(lines, nro_lineas)
    try:
        page=int(page)
    except:
        page=1

    if int(page)*nro_lineas>roles_total or int(page)>0:
        try:
            users = paginator.page(page)
            fin=int(page)*nro_lineas
            ini =fin-nro_lineas
        except PageNotAnInteger or EmptyPage:
            fin=nro_lineas
            ini=0
            users = paginator.page(1)
    else:
        fin=nro_lineas
        ini=0
        users = paginator.page(1)


    roles_list = Rol.objects.order_by('nombre').all()[ini:fin]

    return render_to_response('HtmlRoles/roles.html',{'roles':roles_list,}, RequestContext(request, {
        'lines': users
    }))




def nuevo_permiso(request):
    if request.method=='POST':
        formulario= PermisoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/permisos/')
    else:
        formulario= PermisoForm(request.POST)
    return render_to_response('HtmlPermisos/nuevopermiso.html',{'formulario':formulario}, context_instance=RequestContext(request))


def editar_contenido(request, id_contenido):
     contenido =ContentType.objects.get(pk=id_contenido)
     if request.method=='POST':
        formulario =TipoContenidoForm(request.POST,instance=contenido)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/contenidos/')
     else:
        formulario = TipoContenidoForm(instance=contenido)
     return render_to_response('HtmlPermisos/editarcontenido.html',{'formulario':formulario}, context_instance=RequestContext(request))


def contenidos(request):
    nro_lineas=10
    lines = []
    page = request.GET.get('page')
    contenido_total = ContentType.objects.count()
    for i in range(contenido_total):
        lines.append(u'Line %s' % (i + 1))
    paginator = Paginator(lines, nro_lineas)
    try:
        page=int(page)
    except:
        page=1

    if int(page)*nro_lineas>contenido_total or int(page)>0:
        try:
            users = paginator.page(page)
            fin=int(page)*nro_lineas
            ini =fin-nro_lineas
        except PageNotAnInteger or EmptyPage:
            fin=nro_lineas
            ini=0
            users = paginator.page(1)
    else:
        fin=nro_lineas
        ini=0
        users = paginator.page(1)


    contenidos_list = ContentType.objects.order_by('name').all()[ini:fin]

    return render_to_response('HtmlPermisos/contenidos.html',{'contenidos':contenidos_list,}, RequestContext(request, {
        'lines': users
    }))




def editar_permiso(request, id_permiso):
     permiso =Permission.objects.get(pk=id_permiso)
     if request.method=='POST':
        formulario = PermisoForm(request.POST,instance=permiso)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/contenidos/')
     else:
        formulario = PermisoForm(instance=permiso)
     return render_to_response('HtmlPermisos/editarpermiso.html',{'formulario':formulario}, context_instance=RequestContext(request))


def permisos(request):
    nro_lineas=10
    lines = []
    page = request.GET.get('page')
    permisos_total = Permission.objects.count()
    for i in range(permisos_total):
        lines.append(u'Line %s' % (i + 1))
    paginator = Paginator(lines, nro_lineas)
    try:
        page=int(page)
    except:
        page=1

    if int(page)*nro_lineas>permisos_total or int(page)>0:
        try:
            users = paginator.page(page)
            fin=int(page)*nro_lineas
            ini =fin-nro_lineas
        except PageNotAnInteger or EmptyPage:
            fin=nro_lineas
            ini=0
            users = paginator.page(1)
    else:
        fin=nro_lineas
        ini=0
        users = paginator.page(1)


    permisos_list = Permission.objects.order_by('content_type').all()[ini:fin]

    return render_to_response('HtmlPermisos/permisos.html',{'permisos':permisos_list}, RequestContext(request, {
        'lines': users
    }))


