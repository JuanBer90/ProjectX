from demo_project.demo_app import constantes

__author__ = 'carlos'
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from demo_project.demo_app.models import AtributosPorItem, Item, LineaBase, Fase


def nuevo_lb(request):
    """
    Crea un nuevo Linea Base con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    estado=constantes.EstadosLB().ABIERTO
    if request.method=='POST':
        lb=LineaBase()
        lb.nombre=request.POST.get('nombre','')
        lb.numero =request.POST.get('numero','')
        lb.estado =estado

        lb.save()
        return HttpResponseRedirect ('/privado')
    return render_to_response('HtmlLineaBase/nuevoLB.html',{'estado':estado}, context_instance=RequestContext(request))



