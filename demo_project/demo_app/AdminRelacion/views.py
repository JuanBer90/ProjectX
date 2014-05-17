from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from demo_project.demo_app.AdminRelacion.forms import RelacionForm
from demo_project.demo_app.models import Relacion, Item


def nuevoRelacion(request):
    """
    Crea un nuevo Usuario con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos

    """
    items=Item.objects.all()
    if request.method=='POST':
        relac=Relacion()
        relac.tipo=request.POST.get('tipo','')
        relac.nombre=request.POST.get('nombre','')
        anterior=int(request.POST.get('anterior',''))
        posterior=int(request.POST.get('posterior',''))
        if(anterior != '' and posterior !=''):
            relac.anterior_id=int(anterior)
            relac.posterior_id=int(posterior)
            relac.save()

        return HttpResponseRedirect('/relacion')

    return render_to_response('HtmlRelacion/nuevorelacion.html',{'items':items}, context_instance=RequestContext(request))


def editarrelacion(request,id):
    """
    Edita una nueva Relacion con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos

    """
    items=Item.objects.all()
    relac=Relacion.objects.get(pk=id)
    if request.method=='POST':
        relac.tipo=request.POST.get('tipo','')
        relac.nombre=request.POST.get('nombre','')
        anterior=int(request.POST.get('anterior',''))
        posterior=int(request.POST.get('posterior',''))
        if(anterior != '' and posterior !=''):
            relac.anterior_id=int(anterior)
            relac.posterior_id=int(posterior)
            relac.save()

        return HttpResponseRedirect('/relacion')

    return render_to_response('HtmlRelacion/editarrelacion.html',{'items':items,'relacion':relac}, context_instance=RequestContext(request))


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

    return render_to_response('HtmlRelacion/relacion.html',{'relacion':proyectos_list}, RequestContext(request, {
        'lines': items
    }))



def eliminarrelacion(request, id_tipoitem):
    proyecto= Relacion.objects.get(pk=id_tipoitem)
    if request.method=='POST':
        delete= request.POST['delete']
        if delete == 'si':
            proyecto.delete()

        return HttpResponseRedirect('/relacion/')

    return render_to_response('HtmlRelacion/eliminarrelacion.html',{'proyecto':proyecto},
                              context_instance=RequestContext(request))