from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.views.generic.dates import timezone_today
from demo_project.demo_app import constantes
from demo_project.demo_app.AdminRelacion.forms import RelacionForm
from demo_project.demo_app.constantes import  RelacionEstados, EstadosItem, OperacionItem, execute_one
from demo_project.demo_app.models import Relacion, Item, HistorialItem, Proyecto, Fase


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
    relac=Relacion.objects.get(pk=id)
    fase=Fase.objects.get(pk=relac.actual.fase_id)
    if request.method=='POST':
        relac.tipo=request.POST.get('tipo','')
        relac.nombre=request.POST.get('nombre','')
        relac.save()
        return HttpResponseRedirect('/proyecto/relaciones/'+str(fase.proyecto_id))

    return render_to_response('HtmlRelacion/editar_relacion_proyecto.html',{'relacion':relac}, context_instance=RequestContext(request))


def questions(request):
    if (request.method == 'POST'):
        tipo=request.POST.get('tipo','')



def relacion_item(request,id):
    """
    Edita una nueva Relacion con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos

    """

    actual=Item.objects.get(pk=id)
    post=False

    if request.method=='POST':
        ok=request.POST.get('ok','volver')
        if ok == 'Ok':
            tipo_=request.POST.get('tipo',RelacionEstados().A_S)
            a_o_d=request.POST.get('a_o_d','ANTES')
            if(a_o_d == 'ANTES'):
                antes=1
            else:
                antes=0
            if(tipo_ == RelacionEstados().A_S):
                tipo=1
            else:
                tipo=0
            return HttpResponseRedirect('/relacion/items/' + str(actual.tipo_item_id)+'/'+str(tipo)+'/'+str(antes))
        else:
            return HttpResponseRedirect('/tipoitem/items/'+str(actual.tipo_item_id))

    tipos_relacion=RelacionEstados().estados_relacion()

    return render_to_response('HtmlRelacion/relacion_items.html',{'tipos_relacion':tipos_relacion,
        'actual':actual}, context_instance=RequestContext(request))


def relacion_item_2(request,id,tipo,antes):
    if int(tipo) == 1:
        tipo_ = RelacionEstados().A_S
    else:
        tipo_ = RelacionEstados().P_H
    print 'TIPO: '+str(tipo)+" tipo_ : "+str(tipo_)
    actual=Item.objects.get(pk=id)
    if tipo == 1:
        if request.method=='POST':
                    relac = Relacion()
                    relac.tipo=RelacionEstados().A_S
                    relac.nombre=request.POST.get('nombre','')
                    anterior=int(request.POST.get('anterior',''))
                    posterior=int(request.POST.get('posterior',''))
                    if(antes == 1):
                        relac.despues_id=actual.id_item
                        relac.antes_id=anterior
                    else:
                        relac.despues_id = posterior
                        relac.antes_id = actual.id_item
                    relac.save()

                    return HttpResponseRedirect('/tipoitem/items/'+str(actual.tipo_item_id))
        query = get_query(actual.fase.numero, id)
        print query
        items = Item.objects.raw(query)
        return render_to_response('HtmlRelacion/relacion_items2.html', {'items': items, 'actual': actual,'tipo':tipo_,
           'antes': antes},  context_instance=RequestContext(request))
    else:
        if request.method == 'POST':
                relac = Relacion()
                relac.tipo = RelacionEstados().P_H
                relac.nombre = request.POST.get('nombre', '')
                anterior = int(request.POST.get('anterior', ''))
                posterior = int(request.POST.get('posterior', ''))
                if (antes == 1):
                    relac.despues_id = actual.id_item
                    relac.antes_id = anterior
                else:
                    relac.despues_id = posterior
                    relac.antes_id = actual.id_item
                relac.save()
                return HttpResponseRedirect('/tipoitem/items/' + str(actual.tipo_item_id))

        query = get_query(actual.fase.numero, id)
        print query
        items = Item.objects.raw(query,'padre_hijo')

        return render_to_response('HtmlRelacion/relacion_items2.html',{'items':items,'actual':actual,'tipo':tipo_,
                    'antes':antes}, context_instance=RequestContext(request))


def relacion(request):
    nro_lineas=10
    lines = []
    page = request.GET.get('page')

    objetos_total = Relacion.objects.count()

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

    objetos_list = Relacion.objects.order_by('nombre').all()[ini:fin]
    return render_to_response('HtmlRelacion/relacion.html',{'relacion':objetos_list}, RequestContext(request, {
        'lines': items
    }))


def eliminarrelacion(request, id):
    proyecto= Relacion.objects.get(pk=id)
    if request.method=='POST':
        delete= request.POST['delete']
        if delete == 'si':
            try:
                proyecto.delete()
            except ValueError:
                print ValueError.message
        return HttpResponseRedirect('/relacion/')

    return render_to_response('HtmlRelacion/eliminarrelacion.html',{'proyecto':proyecto},
                              context_instance=RequestContext(request))


def padre_hijo(request,id):
    actual=Item.objects.get(pk=id)
    tipo=RelacionEstados().P_H
    items=Item.objects.filter(fase_id=actual.fase_id, estado=EstadosItem().ITEM_NI).exclude(id_item=id)

    if request.method == 'POST':
        print 'HOLAAAA'
        antes=int(request.POST.get('padre',0))

        if antes != 0:

            item_antes=Item.objects.get(pk=antes)
            relacion=Relacion()
            relacion.actual=actual
            relacion.tipo_relacion=tipo
            relacion.antes=item_antes
            relacion.save()
            historial=HistorialItem()
            historial.user=request.user
            historial.fecha_modificacion=timezone_today()
            historial.item=actual
            historial.tipo_modificacion = OperacionItem().RELACIONAR+str(item_antes.nombre)+' DE LA FASE '+str(item_antes.fase.nombre)
            historial.save()
            return HttpResponseRedirect('/tipoitem/items/'+str(actual.tipo_item_id))


    return render_to_response('HtmlRelacion/padrehijo.html', {'actual': actual,'tipo':tipo,'items':items},
                              context_instance=RequestContext(request))


def get_query(nro_fase,id_item,rel=''):
    if(rel == '' or 'a_o_s'):
        igual="<"
    else:
        igual=""
    query="WITH  T1  AS( select distinct i. *  from item i left join relacion r on r.antes_id = i.id_item "\
    "left join relacion r2 on r2.despues_id = i.id_item right outer join  fase f on f.id_fase = i.fase_id "\
    "where i.estado not like 'ELIMINADO' and f.numero "+igual+"= "+str(nro_fase)+" order  by i.nombre "\
    ") SELECT DISTINCT T1. * FROM T1 JOIN relacion r3 on r3.antes_id = T1.id_item WHERE r3.antes_id != "+str(id_item)
    print query
    return query

def relacion_proyecto(request,id):
    proyecto=Proyecto.objects.get(pk=id)
    nro_lineas=10
    lines = []
    page = request.GET.get('page')
    query="select distinct r.* from relacion r join item i on i.id_item = r.antes_id or i.id_item = r.actual_id " \
          "join fase f on f.id_fase = i.fase_id join proyectos p on p.id_proyecto = f.proyecto_id where p.id_proyecto = "+str(id)
    print query
    query_cont="select (count(t.*) :: int) from ( "+query+" ) as t "
    print query_cont
    objetos_total = execute_one(query_cont)[0]

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

    objetos_list = Relacion.objects.raw(query)[ini:fin]
    return render_to_response('HtmlRelacion/relacion_proyecto.html',{'relacion':objetos_list,'id_proyecto':id}, RequestContext(request, {
        'lines': items
    }))


def eliminar_relacion_proyecto(request, id,id_proyecto):
    proyecto= Relacion.objects.get(pk=id)
    if request.method=='POST':
        delete= request.POST['delete']
        if delete == 'si':
            try:
                proyecto.delete()
            except ValueError:
                print ValueError.message
        return HttpResponseRedirect('/proyecto/relaciones/'+str(id_proyecto))

    return render_to_response('HtmlRelacion/eliminarrelacion.html',{'proyecto':proyecto},
                              context_instance=RequestContext(request))
