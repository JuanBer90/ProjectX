from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponse
from django.views.generic.dates import timezone_today
import xlwt
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
        historial.usuario=request.user
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
        historial = HistorialLineaBase()
        historial.fecha_modificacion = timezone_today()
        historial.linea_base = lb
        historial.usuario = request.user
        historial.tipo_operacion = OperacionLB().MODIFICACION
        historial.save()
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
            historial.usuario=request.user
            historial.tipo_operacion = OperacionLB().ADD_ITEM
            historial.save()
        return  HttpResponseRedirect('/lineabase/items/'+str(lb.id_linea_base))
    return render_to_response('HtmlLineaBase/add_to_lb.html',{}, context_instance=RequestContext(request))

def cerrar(request, id):
    lb=LineaBase.objects.get(pk=id)
    query="WITH Q1 AS (select count(lb.*) from linea_base lb "\
          "join item i on i.linea_base_id = lb.id_linea_base "\
          "where lb.id_linea_base=1 ), "\
          "Q2 AS (select count(lb.*) from linea_base lb "\
          "join item i on i.linea_base_id = lb.id_linea_base "\
          "where lb.id_linea_base=2 and i.estado like 'FINALIZADO') "\
          "SELECT CASE WHEN (COUNT(Q1.*) - COUNT(Q2.*)) = 0 THEN TRUE ELSE FALSE END FROM Q1,Q2"
    se_puede=execute_one(query)[0]
    if request.method == 'POST':
        fin=request.POST.get('fin','no')
        if fin == 'si':
            lb.estado=EstadosLB().CERRADO
            lb.save()
            historial=HistorialLineaBase()
            historial.fecha_modificacion=timezone_today()
            historial.usuario=request.user
            historial.tipo_operacion='CIERRE DE UNA LINEA BASE'
            historial.linea_base=lb
            historial.save()
        return HttpResponseRedirect('/lineabase/listar/'+str(lb.proyecto_id))


    return render_to_response('HtmlLineaBase/cerrar.html', {'se_puede':se_puede}, context_instance=RequestContext(request))

def historial(request,id):

    nro_lineas=10
    lines = []
    page = request.GET.get('page')
    lb = LineaBase.objects.get(pk=id)
    objetos_total = HistorialLineaBase.objects.filter(linea_base=lb).count()

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

    objetos_list = HistorialLineaBase.objects.filter(linea_base=lb)[ini:fin]
    id_proyecto = lb.proyecto_id
    return render_to_response('HtmlLineaBase/historial.html',{'datos':objetos_list,'id_proyecto':id_proyecto,'id_lb':id,'lb':lb}, RequestContext(request, {
        'lines': items
    }))


def lb_reporte(request,id):
    lb=LineaBase.objects.get(pk=id)
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet('Libro1')
    default_style = xlwt.Style.default_style
    negrita= xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;'
                        'font: colour white, bold True;')
    titulos=['Nro','Numero','Operacion','Usuario','Fecha']
    for col, datos in enumerate(titulos):
         sheet.write(0, col, datos, style=negrita)

    values_list=execute_query("select lb.numero, h.tipo_operacion,u.username,h.fecha_modificacion from historial_lb h "
                              "join auth_user u on u.id = h.usuario_id join linea_base lb on lb.id_linea_base=h.linea_base_id  where h.linea_base_id = "+str(id))


    proyecto=Proyecto.objects.get(pk=lb.proyecto_id)
    for row,rowdata in enumerate(values_list):
        cont=0
        for col, val in enumerate(rowdata):
            style = default_style
            cont+=1
            sheet.write(row+1, col+1, str(val), style=style)
        sheet.write(row+1, 0, str(row+1), style=style)
    response = HttpResponse(mimetype='application/vnd.ms-excel')
    name = 'Historial_linea_base'+str(lb.numero)
    response['Content-Disposition'] = 'attachment; filename='+name+'.xls'
    book.save(response)
    return response
