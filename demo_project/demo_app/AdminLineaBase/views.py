from demo_project.demo_app import constantes
from demo_project.demo_app.constantes import EstadosLB

__author__ = 'carlos'
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from demo_project.demo_app.models import  LineaBase, Proyecto, Item


def nuevo_lb(request,id):
    """
    Crea un nuevo Linea Base con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    estado=constantes.EstadosLB().ABIERTO
    if request.method=='POST':
        lb=LineaBase()
        lb.nombre=request.POST.get('nombre','')
        lb.estado =EstadosLB().ABIERTO
        lb.proyecto_id=id
        lb.save()
        return HttpResponseRedirect ('/proyecto/miproyecto/'+str(id))
    return render_to_response('HtmlLineaBase/nuevoLB.html',{'estado':estado}, context_instance=RequestContext(request))

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
    #items=Item.objects.filter().all()
    items=Item.objects.raw("select i.* from item i join fase f on f.id_fase=i.fase_id "
                           "join proyectos p on p.id_proyecto = f.proyecto_id "
                           "where p.id_proyecto = "+str(lb.proyecto_id)+" and i.estado like 'APROBADO' ")
    return render_to_response('HtmlLineaBase/items.html', {'lb': lb, 'items': items},
                              context_instance=RequestContext(request))









