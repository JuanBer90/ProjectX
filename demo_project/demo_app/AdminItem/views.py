import cgi
import os
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.views.generic.dates import timezone_today
from demo_project.demo_app import constantes
from demo_project.demo_app.AdminItem.forms import ItemForm
from demo_project.demo_app.constantes import EstadosItem, execute_query, RelacionEstados, execute_one, OperacionItem
from demo_project.demo_app.models import TipoItem, Item, Fase, HistorialItem, LineaBase, Relacion, Proyecto


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
        item.descripcion =request.POST.get('descripcion','')
        item.tipo_item=tipo_item
        item.fase_id=tipo_item.fase_id
        item.save()
        historial=HistorialItem()
        historial.fecha_modificacion=timezone_today()
        historial.item=item
        historial.tipo_modificacion=EstadosItem().ITEM_NI
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
    fase=Fase.objects.get(pk=item.fase_id)
    tipo_items=TipoItem.objects.all()
    if request.method=='POST':
        historial = HistorialItem()
        historial.tipo_modificacion = "Modificacion nombre anterior: "+str(item.nombre)+' descripcion: '+str(item.descripcion)
        item.nombre=request.POST.get('nombre','')
        item.descripcion =request.POST.get('descripcion','')
        item.save()
        historial.fecha_modificacion=timezone_today()
        historial.item=item
        historial.user=request.user
        historial.save()
        return HttpResponseRedirect('/proyecto/items/'+str(fase.proyecto_id))

    return render_to_response('HtmlItem/editItem.html',{'datos':tipo_items,'item':item}, context_instance=RequestContext(request))
def eliminar_item(request, id):
    objeto= Item.objects.get(pk=id)
    fase=Fase.objects.get(pk=objeto.fase_id)
    if request.method=='POST':
        delete= request.POST['delete']
        if delete == 'si':
            objeto.estado=constantes.EstadosItem().ITEM_EL
            objeto.save()
        return HttpResponseRedirect('/proyecto/items/'+str(fase.proyecto_id))

    return render_to_response('HtmlItem/eliminaritem.html',{'item':objeto},
                              context_instance=RequestContext(request))

def revivir_item(request, id):
    objeto= Item.objects.get(pk=id)
    fase=Fase.objects.get(pk=objeto.fase_id)
    if request.method=='POST':
        delete= request.POST['revivir']
        if delete == 'si':
            objeto.estado=constantes.EstadosItem().ITEM_NI
            objeto.save()
            historial=HistorialItem()
            historial.user=request.user
            historial.tipo_modificacion=OperacionItem.REVIVIR
            historial.fecha_modificacion=timezone_today()
            historial.item=objeto
            historial.save()
        return HttpResponseRedirect('/proyecto/items/'+str(fase.proyecto_id))

    return render_to_response('HtmlItem/revivir.html',{'item':objeto},
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
    id_proyecto = execute_one( "select p.id_proyecto from proyectos p join fase f on f.proyecto_id = p.id_proyecto "
                               "join item i on i.fase_id = f.id_fase where i.id_item = " + str(id))[0]
    return render_to_response('HtmlItem/historial.html',{'datos':objetos_list,'id_proyecto':id_proyecto}, RequestContext(request, {
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

def aprobar_principal(request,id):
    """
    Edita un nuevo Item con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    item=Item.objects.get(pk=id)
    fase=Fase.objects.get(pk=item.fase_id)

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

        return HttpResponseRedirect('/proyecto/items/'+str(fase.proyecto_id))

    return render_to_response('HtmlItem/aprobar.html',{'item':item}, context_instance=RequestContext(request))


def upload(request):
    if(request.method == 'POST'):
        arch=request.FILES.get('file')
        if(arch != None):
            print 'SIZE: '+str(arch)
    return render_to_response('HtmlItem/upload.html', context_instance=RequestContext(request))

def add_lb(request,id):
    item=Item.objects.get(pk=id)
    fase=Fase.objects.get(pk=item.fase_id)
    lbs=LineaBase.objects.filter(proyecto_id=fase.proyecto_id)
    if request.method == 'POST':
        id_lb=int(request.POST.get('lb',0))
        if id_lb != 0:
            item.linea_base_id=id_lb
            item.estado=EstadosItem().ITEM_BL
            item.save()
        return HttpResponseRedirect('/tipoitem/items/' + str(item.tipo_item_id))

    return render_to_response('HtmlItem/add_lb.html', {'item': item,'lbs':lbs,'fase':fase}, context_instance=RequestContext(request))

def antec_suc(request,id):

    actual=Item.objects.get(pk=id)
    fase=Fase.objects.get(pk=actual.fase_id)
    query = "select i.id_item, i.nombre from item i join fase f on f.id_fase=i.fase_id " \
            "join linea_base lb on lb.id_linea_base = i.linea_base_id "\
            " join proyectos p on p.id_proyecto = f.proyecto_id where p.id_proyecto = 1 and i.estado " \
            "like '" + EstadosItem().ITEM_BL + "' and f.numero <= " + str(fase.numero) + "  and i.id_item != " + str(id)+""\
            "and lb.id_linea_base = "+str(actual.linea_base_id)+" and not exists (select r.actual_id from relacion r where r.actual_id = "+str(id)+") "
    print query
    lbs = execute_query(query)
    relacion=Relacion()
    relacion.nombre=''
    relacion.tipo_relacion=RelacionEstados().A_S

    if request.method == 'POST':
        antes=int(request.POST.get('antes',0))
        nombre=request.POST.get('nombre','')
        if antes !=0:
            item_antes=Item.objects.get(pk=antes)
            relacion.antes_id=antes
            relacion.nombre=nombre
            relacion.save()
            historial=HistorialItem()
            historial.tipo_modificacion=OperacionItem.RELACIONAR+' '+str(item_antes.nombre)
            historial.item=actual
            historial.fecha_modificacion=timezone_today()
            historial.user=request.user
            historial.save()
    return render_to_response('HtmlRelacion/antecesor_sucesor.html', {'relacion': relacion,'lbs':lbs,'nombre':actual.nombre,},
                              context_instance=RequestContext(request))

def item_proyecto(request,id):
    nro_lineas=10
    lines = []
    page = request.GET.get('page')
    query = "select i.* from item i join fase f on f.id_fase = i.fase_id " \
            "join proyectos p on p.id_proyecto=f.proyecto_id where p.id_proyecto = " + str(id)
    objetos_total = execute_one("select count(t.*) as cantidad from ("+query+") as t")[0]

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
    objetos_list = Item.objects.raw(query)[ini:fin]


    return render_to_response('HtmlItem/items_proyecto.html',{'datos':objetos_list,'id_proyecto':id}, RequestContext(request, {
        'lines': items
    }))

def finalizar(request,id):
    item=Item.objects.get(pk=id)
    print 'asdfasdf'
    if request.method == 'POST':

        fin=request.POST.get('fin','no')
        if fin == 'si':
            item.estado=EstadosItem().ITEM_FI
            item.save()
            historial=HistorialItem()
            historial.item=item
            historial.tipo_modificacion=OperacionItem().FINALIZAR
            historial.fecha_modificacion=timezone_today()
            historial.user=request.user
            historial.save()

        fase=Fase.objects.get(pk=item.fase_id)
        return HttpResponseRedirect('/proyecto/items/'+str(fase.proyecto_id))
    return render_to_response('HtmlItem/finalizar.html', {'item': item},
                          context_instance=RequestContext(request))