from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from demo_project.demo_app.AdminTipoItem.forms import TipoItemForm
from demo_project.demo_app.constantes import EstadosItem
from demo_project.demo_app.models import TipoItem, Fase, Proyecto, Item


def nuevoTipoItem(request,id):
    """
    Crea un nuevo Tipo Item con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    fases=Fase.objects.all()
    proyectos=Proyecto.objects.all()
    tipo_items=TipoItem.objects.all()
    if request.method=='POST':
        tipo_item=TipoItem()
        proyecto=request.POST.get('proyecto', None)
        fase=request.POST.get('fase', None)
        padre=request.POST.get('padre','')

        tipo_item.nombre=request.POST.get('nombre','')
        tipo_item.descripcion=request.POST.get('descripcion','')
        if proyecto != None:
            tipo_item.proyecto_id=proyecto
        if fase != None:
            tipo_item.fase_id=fase
        if padre != '':
            tipo_item.padre_id=padre

        tipo_item.save()
        return HttpResponseRedirect('/tipoitem/editar/'+str(tipo_item.id_tipo_item))

    return render_to_response('HtmlTipoItem/nuevotipoitem.html',{'fases':fases,'proyectos':proyectos,'tipo_items':tipo_items}, context_instance=RequestContext(request))

def editartipoitem(request, id_tipoitem):
    fases=Fase.objects.all()
    proyectos=Proyecto.objects.all()

    tipo_items=TipoItem.objects.all()
    tipo_item=TipoItem.objects.get(pk=id_tipoitem)
    if request.method=='POST':
        proyecto=request.POST.get('proyecto', None)
        fase=request.POST.get('fase', None)
        padre=request.POST.get('padre','')

        tipo_item.nombre=request.POST.get('nombre','')
        tipo_item.descripcion=request.POST.get('descripcion','')
        if proyecto != None:
            tipo_item.proyecto_id=proyecto
        if fase != None:
            tipo_item.fase_id=fase
        if padre == '':
            tipo_item.padre_id=None
        else:
            tipo_item.padre_id=padre

        tipo_item.save()
        return HttpResponseRedirect('/fases/tipoitems/'+str(tipo_item.fase_id))

    return render_to_response('HtmlTipoItem/editartipoitem.html',
                              {'fases':fases,'tipo_item':tipo_item,'proyectos':proyectos,'tipo_items':tipo_items},
                              context_instance=RequestContext(request))


def tipoitem(request):
    nro_lineas=10
    lines = []
    page = request.GET.get('page')
    objetos_total = TipoItem.objects.count()
    for i in range(objetos_total):
        lines.append(u'Line %s' % (i + 1))
    paginator = Paginator(lines, nro_lineas)
    try:
        page=int(page)
    except:
        page=1

    if int(page)*nro_lineas>objetos_total or int(page)>0:
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

    objetos_list = TipoItem.objects.all()[ini:fin]
    return render_to_response('HtmlTipoItem/tipoitem.html',{'datos':objetos_list}, RequestContext(request, {
        'lines': items
    }))


def eliminartipoitem(request, id_tipoitem):
    proyecto= TipoItem.objects.get(pk=id_tipoitem)

    if request.method=='POST':
        id_fase= proyecto.fase_id
        delete= request.POST['delete']
        if delete == 'si':
            proyecto.delete()

        return HttpResponseRedirect('/fases/tipoitems/'+str(id_fase))

    return render_to_response('HtmlTipoItem/eliminartipoitem.html',{'proyecto':proyecto},
                              context_instance=RequestContext(request))



def TipoItemToFase(request,id):
    """
    Crea un nuevo Usuario con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    fase=Fase.objects.get(pk=id)
    tipo_items=TipoItem.objects.all()
    if request.method=='POST':
        tipo_item=TipoItem()
        padre=request.POST.get('padre','')

        tipo_item.nombre=request.POST.get('nombre','')
        tipo_item.descripcion=request.POST.get('descripcion','')
        tipo_item.proyecto=fase.proyecto
        tipo_item.fase=fase
        if padre != '':
            tipo_item.padre_id=padre

        tipo_item.save()
        return HttpResponseRedirect('/fases/tipoitems/'+str(fase.id_fase))

    return render_to_response('HtmlTipoItem/tipoitemtofase.html',
                              {'fase':fase,'tipo_items':tipo_items}, context_instance=RequestContext(request))


def TipoItemToItem(request,id):
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
        tipo_item=TipoItem.objects.get(pk=id)
        items=Item.objects.filter(tipo_item=tipo_item)
        items_total = items.count()
    else:
        tipo_item=TipoItem.objects.get(pk=id)
        items=Item.objects.filter(tipo_item=tipo_item)
        items_list = items.filter(nombre=buscar)
        items_total = items_list.count()

    for i in range(items_total):
        lines.append(u'Line %s' % (i + 1))
    paginator = Paginator(lines, nro_lineas)
    try:
        page=int(page)
    except:
        page=1

    if int(page)*nro_lineas>items_total or int(page)>0:
        try:
            itemspagination = paginator.page(page)
            fin=int(page)*nro_lineas
            ini =fin-nro_lineas
        except PageNotAnInteger or EmptyPage:
            fin=nro_lineas
            ini=0
            itemspagination = paginator.page(1)
    else:
        fin=nro_lineas
        ini=0
        itemspagination = paginator.page(1)
    if buscar == '':
        tipo_item=TipoItem.objects.get(pk=id)
        items=Item.objects.filter(tipo_item=tipo_item).all()[ini:fin]
        estado_item=EstadosItem().ITEM_NI

    else:
        tipo_item=TipoItem.objects.get(pk=id)
        #items=Item.objects.filter(tipo_item=tipo_item,nombre=buscar)[ini:fin]
        items=Item.objects.raw("select * from item where nombre like '%%"+buscar+"%%'" )
        estado_item=EstadosItem().ITEM_NI
        print 'buscar: '+str(buscar)
    return render_to_response('HtmlTipoItem/tipo_item_to_item.html',{'tipo_item':tipo_item,'datos':items,'estado_item':estado_item}, context_instance=RequestContext(request, {
        'lines': itemspagination
    }))

