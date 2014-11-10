from django.shortcuts import render, render_to_response
from AdminFases.models import Fase
from django.template.context import RequestContext
from AdminTipoItem.models import TipoItem
from AdminProyectos.models import Proyecto
from AdminTipoItem.forms import TipoItemForm
from django.contrib import messages
from string import upper
from AdminItems.models import Item, HistorialItem
from AdminItems.forms import ItemForm
from django.views.generic.dates import timezone_today
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
#===============================================================================
def items_proyecto(request,id_proyecto):
     tipoitems=TipoItem.objects.filter(fase__proyecto_id=id_proyecto)
     fases=Fase.objects.filter(proyecto_id=id_proyecto,estado='INI')
     items=Item.objects.filter(tipo_item__fase__proyecto_id=id_proyecto)
     proyecto=Proyecto.objects.get(pk=id_proyecto)
     form=ItemForm()
     if request.method == 'POST':
         nombre=request.POST.get('nombre','')
         descripcion=request.POST.get('descripcion','')
         prioridad=request.POST.get('prioridad','')
         costo=request.POST.get('costo','')
         complejidad=request.POST.get('complejidad','')
         
         id_item=request.POST.get('id_item','')
         id_tipo=request.POST.get('tipo','')
         id_delete=request.POST.get('id_delete','')
         print "item"
         print id_item
         
         if id_tipo != '':
             if id_item != "":
                 item=Item.objects.get(pk=id_tipo)
                 messages.success(request,"Item Editado con exito!")
             else:
                 item=Item()
                 messages.success(request,"Item "+upper(item.nombre)+" creado con exito!")
                
             item.nombre=nombre
             item.tipo_item_id=id_tipo
             item.prioridad=prioridad
             item.complejidad=complejidad
             item.costo=costo
             item.descripcion=descripcion
             item.save()
             if id_item == "":
                 save_historial("CREACION",request.user.id,item.id)
             else:
                 save_historial("MODIFICACION",request.user.id,item.id) 
         
         if id_delete != "":
             aux=Item.objects.get(pk=id_delete)
             messages.error(request,"Item Eliminado "+aux.nombre+" con exito!")
             aux.estado='ELI'
             aux.save()
             save_historial("ELIMINACION",request.user.id,item.id)
         
     buscar=''
     filtro_tipo_id=""
     if request.method == 'GET':
        buscar=request.GET.get('buscar','')
        filtro_tipo_id=request.GET.get('filtro-tipo','')
     
     if filtro_tipo_id != "":
         
         items_list = Item.objects.filter(nombre__icontains=buscar,tipo_item_id=filtro_tipo_id)
     else:
         items_list = Item.objects.filter(nombre__icontains=buscar)
     paginator = Paginator(items_list, 10) # Show 25 contacts per page

     page = request.GET.get('page','')
     try:
        page=int(page)
     except:
         page=1    
     try:
         items = paginator.page(page)
     except PageNotAnInteger:
        # If page is not an integer, deliver first page.
         items = paginator.page(1)
     except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)

     return render_to_response('HtmlItem/itemsproyecto.html',
                               {'tipo_items':tipoitems,'proyecto':proyecto,'fases':fases,'items':items,'total':items_list.count(),
                                'form':form,'page_range':paginator.page_range,'page':int(page),'buscar':buscar,'placeholder':'Nombre'},
                              context_instance=RequestContext(request))

def save_historial(tipo,id_usuario,id_item):
    h=HistorialItem()
    h.fecha_modificacion=timezone_today()
    h.tipo_modificacion=tipo
    h.user_id=id_usuario
    h.item_id=id_item
    h.save()