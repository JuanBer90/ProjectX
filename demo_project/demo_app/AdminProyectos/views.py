from mx.DateTime.DateTime import today
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from demo_project.demo_app.AdminProyectos.forms import ProyectoForm
from demo_project.demo_app.models import Proyecto


def nuevo_proyecto(request):
    user=request.user
    if request.method=='POST':
        formulario= ProyectoForm(request.POST)
        if formulario.is_valid():
            proyecto= formulario.save()
            proyecto.leader = request.user
            proyecto.estado=True
            proyecto.coste_total=0
            proyecto.fecha_creacion = today()
            proyecto.save()
            return HttpResponseRedirect('/')
    else:
        formulario= ProyectoForm(request.POST)
    return render_to_response('HtmlProyecto/nuevoproyecto.html',{'formulario':formulario,'user':user},
                              context_instance=RequestContext(request))

