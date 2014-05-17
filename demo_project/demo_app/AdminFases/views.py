from mx.DateTime.DateTime import today
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect
from demo_project.demo_app import constantes

from demo_project.demo_app.models import Rol, Permisos, RolUser, Fase


def fases_proyecto(request, id_proyecto):
    """
        Crea el Rol con sus posibles permisos
        """
    fases=Fase.objects.filter(proyecto_id=id_proyecto).order_by('numero')
    return render_to_response('HtmlFases/fasesproyecto.html',{'fases':fases,'id_proyecto':id_proyecto}, context_instance=RequestContext(request))

def fase(request, id_fase,id_proyecto):
    fase=Fase.objects.get(pk=id_fase)
    if fase.nombre == None:
        modo='Crear'
    else:
        modo='Editar'

    msg=''
    if request.method=='POST':
         nombre=request.POST.get('nombre','')
         aux=Fase.objects.filter(nombre=nombre).count()
         if aux >1:
            msg='Ya existe una Fase con el mismo nombre'
            return render_to_response('HtmlFases/editfase.html',{'fase':fase,'modo':modo,'msg':msg,'id_proyecto':id_proyecto},context_instance=RequestContext(request))
         descripcion=request.POST.get('descripcion','')
         fecha=today()
         fase.nombre=nombre
         fase.descripcion=descripcion
         fase.estado=constantes.EstadosFase().FASE_NI
         fase.fecha_creacion=fecha
         fase.save()
         return HttpResponseRedirect('/proyecto/fases/'+str(id_proyecto))

    estados=constantes.EstadosFase()

    return render_to_response('HtmlFases/editfase.html',{'fase':fase,'modo':modo,'msg':msg,'estados':estados.FASE_NI,'id_proyecto':id_proyecto},context_instance=RequestContext(request))



def importar(request, id_fase):
    """
    Buscador de Fases
   """
    fase=Fase.objects.get(pk=id_fase)
    nro_lineas=10
    lines = []
    page = request.GET.get('page')
    if request.method=='POST':
        buscar=request.POST["buscar"]
    else:
        buscar = ''

    if buscar == '':
        fases_total = Fase.objects.all().exclude(nombre=None, proyecto_id=fase.proyecto_id).count()
    else:
        permisos_list = Fase.objects.filter(nombre__contains=buscar)
        fases_total = permisos_list.count()

    for i in range(fases_total):
        lines.append(u'Line %s' % (i + 1))
    paginator = Paginator(lines, nro_lineas)
    try:
        page=int(page)
    except:
        page=1

    if int(page)*nro_lineas>fases_total or int(page)>0:
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
        fases_list = Fase.objects.order_by('nombre').all().exclude(nombre=None,proyecto_id=fase.proyecto_id)[ini:fin]
    else:
        fases_list = Fase.objects.filter(nombre=buscar)[ini:fin]

    return render_to_response('HtmlFases/fases.html',{'fases':fases_list,'id_fase':id_fase}, RequestContext(request, {
        'lines': items
    }))

def procesar_import(request,id_fase,id_import):
    fase=Fase.objects.get(pk=id_fase)
    fase_import=Fase.objects.get(pk=id_import)
    fase.nombre=fase_import.nombre
    fase.descripcion = fase_import.descripcion
    fase.estado = fase_import.estado
    fase.save()
    return HttpResponseRedirect('/proyecto/fases/'+str(fase.proyecto_id))