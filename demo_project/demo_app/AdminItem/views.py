from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.views.generic.dates import timezone_today
from demo_project.demo_app.AdminItem.forms import ItemForm
from demo_project.demo_app.constantes import EstadosItem
from demo_project.demo_app.models import TipoItem, Item, Fase, HistorialItem


def nuevo_item(request,id=0):
    """
    Crea un nuevo Item con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    fases=Fase.objects.all()
    tipo_items=TipoItem.objects.all()
    if request.method=='POST':
        item=Item()
        item.nombre=request.POST.get('nombre','')
        item.numero =request.POST.get('numero','')
        item.descripcion =request.POST.get('descripcion','')
        id_ti=request.POST.get('tipo_item',0)


        if int(id_ti) != 0:
            item.tipo_item_id = int(id_ti)
            item.save()
            historial=HistorialItem()
            historial.fecha_modificacion=timezone_today()
            historial.item=item
            historial.tipo_modificacion="Creacion"
            historial.user=request.user
            historial.save()
    return render_to_response('HtmlItem/editItem.html',{'fases':fases,'datos':tipo_items}, context_instance=RequestContext(request))


def TipoItem_nuevo_item(request,id):
    """
    Crea un nuevo Item con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    tipo_item=TipoItem.objects.get(pk=id)
    if request.method=='POST':
        item=Item()
        item.nombre=request.POST.get('nombre','')
        item.numero =request.POST.get('numero','')
        item.descripcion =request.POST.get('descripcion','')
        item.tipo_item=tipo_item
        item.save()
        historial=HistorialItem()
        historial.fecha_modificacion=timezone_today()
        historial.item=item
        historial.tipo_modificacion="Creacion"
        historial.user=request.user
        historial.save()
        return HttpResponseRedirect('/tipoitem/items/'+str(tipo_item.id_tipo_item))

    return render_to_response('HtmlItem/tipoitem_item.html',{'tipo_item':tipo_item}, context_instance=RequestContext(request))


def TipoItem_editar_item(request,id):
    """
    Crea un nuevo Item con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    item=Item.objects.get(pk=id)
    if request.method=='POST':
        item.nombre=request.POST.get('nombre','')
        item.numero =request.POST.get('numero','')
        item.descripcion =request.POST.get('descripcion','')
        item.save()
        historial=HistorialItem()
        historial.fecha_modificacion=timezone_today()
        historial.item=item
        historial.tipo_modificacion="Modificacion"
        historial.user=request.user
        historial.save()
        return HttpResponseRedirect('/tipoitem/items/'+str(item.tipo_item_id))

    return render_to_response('HtmlItem/tipoitem_item.html',{'item':item,'tipo_item':item.tipo_item}, context_instance=RequestContext(request))



def editar_item(request,id):
    """
    Edita un nuevo Item con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    item=Item.objects.get(pk=id)
    fases=Fase.objects.all()
    tipo_items=TipoItem.objects.all()
    if request.method=='POST':
        item.nombre=request.POST.get('nombre','')
        item.numero =request.POST.get('numero','')
        item.descripcion =request.POST.get('descripcion','')
        id_ti=request.POST.get('tipo_item',0)
        if int(id_ti) != 0:
            item.tipo_item_id = int(id_ti)
            item.save()
            historial=HistorialItem()
            historial.fecha_modificacion=timezone_today()
            historial.item=item
            historial.tipo_modificacion="Modificacion"
            historial.user=request.user
            historial.save()
            return HttpResponseRedirect('/item/listar')

    return render_to_response('HtmlItem/editItem.html',{'fases':fases,'datos':tipo_items,'item':item}, context_instance=RequestContext(request))
def eliminar_item(request, id):
    objeto= TipoItem.objects.get(pk=id)
    if request.method=='POST':
        delete= request.POST['delete']
        if delete == 'si':
            objeto.delete()
        return HttpResponseRedirect('/items/listar')

    return render_to_response('HtmlItem/eliminaritem.html',{'item':objeto},
                              context_instance=RequestContext(request))


def listar_items(request):
    nro_lineas=10
    lines = []
    page = request.GET.get('page')
    objetos_total = Item.objects.count()
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

    objetos_list = Item.objects.all()[ini:fin]
    return render_to_response('HtmlItem/items.html',{'datos':objetos_list}, RequestContext(request, {
        'lines': items
    }))

def historial(request,id):

    nro_lineas=10
    lines = []
    page = request.GET.get('page')
    objetos_total = HistorialItem.objects.filter(item_id=id).count()
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

    objetos_list = HistorialItem.objects.filter(item_id=id)[ini:fin]
    return render_to_response('HtmlItem/historial.html',{'datos':objetos_list}, RequestContext(request, {
        'lines': items
    }))

def aprobar(request,id):
    """
    Edita un nuevo Item con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    item=Item.objects.get(pk=id)

    tipo_items=TipoItem.objects.all()
    if request.method=='POST':
        aprobar=request.POST.get('aprobar','si')

        if aprobar== 'si':
            item.estado=EstadosItem().ITEM_AP
            item.save()
            historial=HistorialItem()
            historial.fecha_modificacion=timezone_today()
            historial.item=item
            historial.tipo_modificacion="APROBACION"
            historial.user=request.user
            historial.save()

        return HttpResponseRedirect('/tipoitem/items/'+str(item.tipo_item_id))

    return render_to_response('HtmlItem/aprobar.html',{'item':item}, context_instance=RequestContext(request))


def upload(request):
    if(request.method == 'POST'):
        arch=request.FILES.get('file')
        if(arch != None):
            print 'SIZE: '+str(arch)
            

    return render_to_response('HtmlItem/upload.html', context_instance=RequestContext(request))
