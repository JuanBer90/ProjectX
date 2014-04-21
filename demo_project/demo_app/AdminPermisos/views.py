from django.contrib.auth.models import User,ContentType, Permission
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from demo_project.demo_app.AdminPermisos.forms import TipoContenidoForm, PermisoForm
from demo_project.demo_app.models import Proyecto


def nuevo_contenido(request):
    if request.method=='POST':
        formulario= TipoContenidoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/contenidos/')
    else:
        formulario= TipoContenidoForm(request.POST)
    return render_to_response('HtmlPermisos/nuevocontenido.html',{'formulario':formulario}, context_instance=RequestContext(request))

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
    if request.method=='POST':
        buscar=request.POST["buscar"]
    else:
        buscar = ''

    if buscar == '':
        proyectos_total = Permission.objects.count()
    else:
        permisos_list = Permission.objects.filter(name=buscar)
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
        proyectos_list = Permission.objects.order_by('name').all()[ini:fin]
    else:
        proyectos_list = Permission.objects.filter(name=buscar)[ini:fin]

    return render_to_response('HtmlPermisos/permisos.html',{'permisos':proyectos_list}, RequestContext(request, {
        'lines': items
    }))

