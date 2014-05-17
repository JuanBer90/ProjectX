from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from demo_project.demo_app.AdminRelacion.forms import RelacionForm
from demo_project.demo_app.models import Relacion


def nuevoRelacion(request):
    """
    Crea un nuevo Usuario con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    if request.method=='POST':
        formulario = RelacionForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/relacion')
    else:
        formulario = RelacionForm(request.POST)
    return render_to_response('HtmlRelacion/nuevorelacion.html',{'formulario':formulario}, context_instance=RequestContext(request))


def relacion(request):
    nro_lineas=10
    lines = []
    page = request.GET.get('page')
    if request.method=='POST':
        buscar=request.POST.get("buscar",'')
        print 'BUSCAR QUE OND: '+buscar
    else:
        buscar = ''

    if buscar == '':
        proyectos_total = Relacion.objects.count()
    else:
        permisos_list = Relacion.objects.filter(nombre=buscar)
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
        proyectos_list = Relacion.objects.order_by('nombre').all()[ini:fin]
    else:
        proyectos_list = Relacion.objects.filter(nombre=buscar)[ini:fin]
    print 'BUSCAR: '+buscar

    return render_to_response('HtmlRelacion/relacion.html',{'tipoitem':proyectos_list}, RequestContext(request, {
        'lines': items
    }))


def editarrelacion(request, id_tipoitem):
     permiso =Relacion.objects.get(pk=id_tipoitem)
     if request.method=='POST':
        formulario = RelacionForm(request.POST,instance=permiso)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/relacion/')
     else:
        formulario = RelacionForm(instance=permiso)
     return render_to_response('HtmlRelacion/editarrelacion.html',{'formulario':formulario}, context_instance=RequestContext(request))


def eliminarrelacion(request, id_tipoitem):
    proyecto= Relacion.objects.get(pk=id_tipoitem)
    if request.method=='POST':
        delete= request.POST['delete']
        if delete == 'si':
            proyecto.delete()

        return HttpResponseRedirect('/relacion/')

    return render_to_response('HtmlRelacion/eliminarrelacion.html',{'proyecto':proyecto},
                              context_instance=RequestContext(request))