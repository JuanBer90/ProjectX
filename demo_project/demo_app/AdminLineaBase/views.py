from django.views.generic.dates import timezone_today
from demo_project.demo_app import constantes
from demo_project.demo_app.constantes import EstadosLB, execute_query, execute_one, EstadosItem, OperacionLB

__author__ = 'carlos'
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from demo_project.demo_app.models import  LineaBase, Proyecto, Item, HistorialLineaBase


def nuevo_lb(request,id):
    """
    Crea un nuevo Linea Base con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    query="select case when max(lb.numero) is null then 1 else max(lb.numero)+1 end " \
          "from linea_base lb join proyectos p on p.id_proyecto = lb.proyecto_id where p.id_proyecto = "+str(id)
    lb = LineaBase()
    lb.numero=execute_one(query)[0]
    lb.estado=EstadosLB().ABIERTO
    if request.method=='POST':
        lb.proyecto_id=id
        lb.save()
        historial=HistorialLineaBase()
        historial.fecha_modificacion=timezone_today()
        historial.linea_base=lb
        historial.tipo_operacion=OperacionLB().CREACION
        historial.save()
        return HttpResponseRedirect ('/proyecto/miproyecto/'+str(id))
    return render_to_response('HtmlLineaBase/nuevoLB.html',{'lb':lb}, context_instance=RequestContext(request))

def editar_lb(request,id):
    lb=LineaBase.objects.get(pk=id)
    if request.method == 'POST':
        lb.nombre = request.POST.get('nombre', '')
        lb.estado = EstadosLB().ABIERTO
        lb.proyecto_id = id
        lb.save()
        return HttpResponseRedirect('/lineabase/listar/' + str(lb.proyecto_id))
    return render_to_response('HtmlLineaBase/nuevoLB.html', {'estado': lb.estado,'lb':lb},
                              context_instance=RequestContext(request))

def listar_lb(request,id):
    proyecto=Proyecto.objects.get(pk=id)
    lbs=LineaBase.objects.filter(proyecto=proyecto)
    return render_to_response('HtmlLineaBase/listarLB.html',{'lbs':lbs,'proyecto':proyecto},context_instance=RequestContext(request))

def items(request, id):
    lb=LineaBase.objects.get(pk=id)
    items=Item.objects.raw("select i.* from item i join fase f on f.id_fase=i.fase_id "
                           "join proyectos p on p.id_proyecto = f.proyecto_id "
                           "where p.id_proyecto = "+str(lb.proyecto_id))

    return render_to_response('HtmlLineaBase/items.html', {'lb': lb, 'items': items,'estado':EstadosItem().ITEM_BL},
                              context_instance=RequestContext(request))

def item_to_lb(request,id_item, id_lb):
    item=Item.objects.get(pk=id_item)
    lb=LineaBase.objects.get(pk=id_lb)
    print 'hola1'
    if request.method == 'POST':
        add=request.POST.get('add','no')
        if add == 'si':
            item.linea_base_id=id_lb
            item.estado=EstadosItem().ITEM_BL
            item.save()
            historial = HistorialLineaBase()
            historial.fecha_modificacion = timezone_today()
            historial.linea_base = lb
            historial.tipo_operacion = OperacionLB().ADD_ITEM
            historial.save()
        return  HttpResponseRedirect('/lineabase/items/'+str(lb.id_linea_base))
    return render_to_response('HtmlLineaBase/add_to_lb.html',{}, context_instance=RequestContext(request))









