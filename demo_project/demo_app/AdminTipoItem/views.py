from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from demo_project.demo_app.AdminTipoItem.forms import TipoItemForm
from demo_project.demo_app.models import TipoItem


def nuevoTipoItem(request):
    """
    Crea un nuevo Usuario con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    if request.method=='POST':
        formulario = TipoItemForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/tipoitem')
    else:
        formulario = TipoItemForm(request.POST)
    return render_to_response('HtmlTipoItem/nuevotipoitem.html',{'formulario':formulario}, context_instance=RequestContext(request))


def tipoitem(request):
    nro_lineas=10
    lines = []
    page = request.GET.get('page')
    if request.method=='POST':
        buscar=request.POST["buscar"]
    else:
        buscar = ''

    if buscar == '':
        proyectos_total = TipoItem.objects.count()
    else:
        permisos_list = TipoItem.objects.filter(nombre=buscar)
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
        proyectos_list = TipoItem.objects.order_by('nombre').all()[ini:fin]
    else:
        proyectos_list = TipoItem.objects.filter(nombre=buscar)[ini:fin]

    return render_to_response('HtmlTipoItem/tipoitem.html',{'tipoitem':proyectos_list}, RequestContext(request, {
        'lines': items
    }))


def editartipoitem(request, id_tipoitem):
     permiso =TipoItem.objects.get(pk=id_tipoitem)
     if request.method=='POST':
        formulario = TipoItemForm(request.POST,instance=permiso)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/tipoitem/')
     else:
        formulario = TipoItemForm(instance=permiso)
     return render_to_response('HtmlTipoItem/editartipoitem.html',{'formulario':formulario}, context_instance=RequestContext(request))


def eliminartipoitem(request, id_tipoitem):
    proyecto= TipoItem.objects.get(pk=id_tipoitem)
    if request.method=='POST':
        delete= request.POST['delete']
        if delete == 'si':
            proyecto.delete()

        return HttpResponseRedirect('/tipoitem/')

    return render_to_response('HtmlTipoItem/eliminartipoitem.html',{'proyecto':proyecto},
                              context_instance=RequestContext(request))