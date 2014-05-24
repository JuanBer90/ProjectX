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
        item=int(request.POST.get('item',0))
        if(item >0):
            relac.item_id=int(item)
            relac.save()
            return HttpResponseRedirect('/atributoitem')


    return render_to_response('HtmlAtributoItem/nuevoatributoitem.html',{'items':items}, context_instance=RequestContext(request))


def editaratributoitem(request,id):
    """
    Edita una nueva Relacion con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos

    """
    atributo=AtributosPorItem.objects.get(pk=id)
    item=atributo.item
    if request.method=='POST':
        atributo.nombre=request.POST.get('nombre','')
        atributo.tipo=request.POST.get('tipo','')
        atributo.valor_defecto=request.POST.get('valor_defecto','')
        atributo.save()
        return HttpResponseRedirect('/atributoitem')


    return render_to_response('HtmlAtributoItem/editaratributoitem.html',{'item':item,'atributo':atributo}, context_instance=RequestContext(request))



def ver_atributo(request,id):
    """
    Edita una nueva Relacion con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos

    """
    atributo=AtributosPorItem.objects.get(pk=id)
    item=atributo.item
    if request.method=='POST':
        return HttpResponseRedirect('/tipoitem/items/'+str(item.tipo_item_id))


    return render_to_response('HtmlAtributoItem/veratributo.html',{'item':item,'atributo':atributo}, context_instance=RequestContext(request))



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

    objetos_list = AtributosPorItem.objects.order_by('tipo').all()[ini:fin]
    return render_to_response('HtmlAtributoItem/atributoitem.html',{'objetos':objetos_list}, RequestContext(request, {
        'lines': items
    }))


def eliminaratributoitem(request, id):
    proyecto= AtributosPorItem.objects.get(pk=id)
    if request.method=='POST':
        delete= request.POST['delete']
        if delete == 'si':
            proyecto.delete()
            return HttpResponseRedirect('/atributoitem/')

    return render_to_response('HtmlAtributoItem/eliminaratributoitem.html',{'proyecto':proyecto},
                              context_instance=RequestContext(request))


def atributos_por_item(request,id):
    item=Item.objects.get(pk=id)
    objetos_list = AtributosPorItem.objects.filter(item=item)
    return render_to_response('HtmlAtributoItem/atributos_por_item.html',{'objetos':objetos_list,'item':item}, RequestContext(request))



def add_atributo_item(request,id):
    """
    Crea un nuevo Usuario con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos

    """
    item=Item.objects.get(pk=id)
    if request.method=='POST':
        atributo=AtributosPorItem()
        atributo.nombre=request.POST.get('nombre','')
        atributo.tipo=request.POST.get('tipo','')
        atributo.valor_defecto=request.POST.get('valor_defecto','')
        atributo.item=item
        atributo.save()
        return HttpResponseRedirect('/atributoitem/atributos/'+str(id))


    return render_to_response('HtmlAtributoItem/add_atributo_item.html',{'item':item}, context_instance=RequestContext(request))


def edit_atributo_item(request,id):
    """
    Crea un nuevo Usuario con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos

    """
    atributo=AtributosPorItem.objects.get(pk=id)
    item=atributo.item
    if request.method=='POST':
        atributo.nombre=request.POST.get('nombre','')
        atributo.tipo=request.POST.get('tipo','')
        atributo.valor_defecto=request.POST.get('valor_defecto','')
        atributo.save()
        return HttpResponseRedirect('/atributoitem/atributos/'+str(item.id_item))


    return render_to_response('HtmlAtributoItem/edit_atributo_item.html',{'item':item,'atributo':atributo}, context_instance=RequestContext(request))

def delete_atributo_item(request, id):
    atributo= AtributosPorItem.objects.get(pk=id)
    if request.method=='POST':
        delete= request.POST['delete']
        if delete == 'si':
            atributo.delete()
            return HttpResponseRedirect('/atributoitem/atributos/'+str(atributo.item_id))

    return render_to_response('HtmlAtributoItem/delete_atributo_item.html',{'atributo':atributo},
                              context_instance=RequestContext(request))
