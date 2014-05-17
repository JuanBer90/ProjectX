from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from demo_project.demo_app.models import AtributosPorItem, Item


def nuevoatributoitem(request):
    """
    Crea un nuevo Usuario con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos

    """
    items=Item.objects.all()
    if request.method=='POST':
        relac=AtributosPorItem()
        relac.nombre=request.POST.get('nombre','')
        relac.tipo=request.POST.get('tipo','')
        relac.valor_defecto=request.POST.get('valor_defecto','')
        item=int(request.POST.get('item',''))
        relac.item_id=int(item)
        relac.save()

        return HttpResponseRedirect('/atributositem')

    return render_to_response('HtmlAtributosItem/nuevoatributositem.html',{'items':items}, context_instance=RequestContext(request))


def editaratributoitem(request,id):
    """
    Edita una nueva Relacion con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos

    """
    items=Item.objects.all()
    relac=AtributosPorItem.objects.get(pk=id)
    if request.method=='POST':
        relac=AtributosPorItem()
        relac.nombre=request.POST.get('nombre','')
        relac.tipo=request.POST.get('tipo','')
        relac.valor_defecto=request.POST.get('valor_defecto','')
        item=int(request.POST.get('item',''))
        relac.item_id=int(item)
        relac.save()

        return HttpResponseRedirect('/atributoitem')

    return render_to_response('HtmlAtributoItem/editaratributoitem.html',{'items':items,'atributoitem':relac}, context_instance=RequestContext(request))


def atributoitem(request):
    nro_lineas=10
    lines = []
    page = request.GET.get('page')

    objetos_total = AtributosPorItem.objects.count()

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

    objetos_list = AtributosPorItem.objects.order_by('nombre').all()[ini:fin]
    return render_to_response('HtmlAtributoItem/atributoitem.html',{'relacion':objetos_list}, RequestContext(request, {
        'lines': items
    }))



def eliminaratributoitem(request, id_tipoitem):
    proyecto= AtributosPorItem.objects.get(pk=id_tipoitem)
    if request.method=='POST':
        delete= request.POST['delete']
        if delete == 'si':
            proyecto.delete()

        return HttpResponseRedirect('/atributoitem/')

    return render_to_response('Html/eliminaratributoitem.html',{'proyecto':proyecto},
                              context_instance=RequestContext(request))
