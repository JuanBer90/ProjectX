from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
            return HttpResponseRedirect('/proyectos')
    else:
        formulario= ProyectoForm(request.POST)
    return render_to_response('HtmlProyecto/nuevoproyecto.html',{'formulario':formulario,'user':user},
                              context_instance=RequestContext(request))


def editar_proyecto(request, id_proyecto):

    proyecto= Proyecto.objects.get(pk=id_proyecto)
    if request.method=='POST':
        formulario= ProyectoForm(request.POST,instance=proyecto)
        if formulario.is_valid():
            proyecto= formulario.save()
            proyecto.save()
            return HttpResponseRedirect('/proyectos/')
    else:
        formulario= ProyectoForm(instance=proyecto)
        user= User()
        user=proyecto.leader
    return render_to_response('HtmlProyecto/editarproyecto.html',{'formulario':formulario,'user':user},
                              context_instance=RequestContext(request))



def proyectos(request):
    nro_lineas=10
    lines = []
    page = request.GET.get('page')
    proyectos_total = Proyecto.objects.count()
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


    proyectos_list = Proyecto.objects.order_by('nombre').all()[ini:fin]

    return render_to_response('HtmlProyecto/proyectos.html',{'proyectos':proyectos_list}, RequestContext(request, {
        'lines': items
    }))


