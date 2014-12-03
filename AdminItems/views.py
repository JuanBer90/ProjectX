from django.shortcuts import render, render_to_response
from AdminFases.models import Fase
from django.template.context import RequestContext
from AdminTipoItem.models import TipoItem
from AdminProyectos.models import Proyecto
from AdminTipoItem.forms import TipoItemForm
from django.contrib import messages
from string import upper
from AdminItems.models import *
from AdminItems.forms import ItemForm, UploadFileForm, DocumentForm
from django.views.generic.dates import timezone_today
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q
from projectx.grafo import Grafo
from projectx.globales import *

# Create your views here.
#===============================================================================
def items_proyecto(request,id_proyecto):
     tipoitems=TipoItem.objects.filter(fase__proyecto_id=id_proyecto)
     fases=Fase.objects.filter(proyecto_id=id_proyecto,estado='INI')
     
     proyecto=Proyecto.objects.get(pk=id_proyecto)
     form=ItemForm()
     file_form = DocumentForm() # A empty, unbound form
     if request.method == 'POST':
         print request.POST.get('file','')
         for a in request.POST:
             print a
     if request.method == 'POST':
         item_file=request.POST.get('id_item_file','')
         
         form = DocumentForm(request.POST, request.FILES)
         if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            print item_file,"   item file"
            if item_file != "":
               newdoc.item_id=item_file
               newdoc.nombre=request.POST.get('nombre_archivo','')
               newdoc.save()
               
               save_historial("ARCHIVO ADJUNTADO",request.user.id,item_file)
               messages.success(request,"Archivo Adjuntado Exitosamente!")

         nombre=request.POST.get('nombre','')
         descripcion=request.POST.get('descripcion','')
         prioridad=request.POST.get('prioridad','')
         costo=request.POST.get('costo','')
         complejidad=request.POST.get('complejidad','')
         
         id_item=request.POST.get('id_item','')
         id_tipo=request.POST.get('tipo','')
         id_delete=request.POST.get('id_delete','')
         id_revive=request.POST.get('id_revive','')
         
         if id_tipo != '':
             print "id_tipo  "+id_tipo
             if id_item != "":
                 item=Item.objects.get(pk=id_tipo)
                 messages.success(request,"Item "+upper(nombre)+" editado con exito!")
                 if not Item.objects.filter(tipo_item__fase_id=item.tipo_item.fase_id).exists():
                     fase2=Fase.objects.get(pk=item.tipo_item.fase_id)
                     fase2.estado="INI"
                     fase2.save()
                     messages.info(request,"INFO: Fase "+upper(fase2.nombre)+" ha pasado a estado 'INICIADO'!")
             
             else:
                 item=Item()
                 messages.success(request,"Item "+upper(nombre)+" creado con exito!")
             fase1=Fase.objects.get(pk=TipoItem.objects.get(pk=id_tipo).fase_id)
             if fase1.estado == 'INI':
                fase1.estado = 'DES'
                fase1.save() 
                
                messages.info(request,"INFO: Fase "+upper(fase1.nombre)+" ha pasado al estado 'DESARROLLO'!")
             
            
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
             save_historial("ELIMINACION",request.user.id,aux.id)
         if id_revive !="":
             aux=Item.objects.get(pk=id_revive)
             messages.success(request,"Item Revivido "+aux.nombre+" con exito!")
             aux.estado='DES'
             aux.save()
             save_historial("REVIVIR",request.user.id,aux.id)
         
     buscar=''
     filtro_tipo_id=""
     if request.method == 'GET':
        buscar=request.GET.get('buscar','')
        filtro_tipo_id=request.GET.get('filtro-tipo','')
     
     if filtro_tipo_id != "":
         
         items_list = Item.objects.filter(nombre__icontains=buscar,tipo_item_id=filtro_tipo_id,tipo_item__fase__proyecto_id=id_proyecto)
     else:
         items_list = Item.objects.filter(nombre__icontains=buscar,tipo_item__fase__proyecto_id=id_proyecto)
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
     for item in items:
         item.archivos=Document.objects.filter(item_id=item.pk)
     return render_to_response('HtmlItem/itemsproyecto.html',
    {'tipo_items':tipoitems,'proyecto':proyecto,'fases':fases,'items':items,'total':items_list.count(),
        'file_form':file_form,'form':form,'page_range':paginator.page_range,'page':int(page),'buscar':buscar,'placeholder':'Nombre'},
                              context_instance=RequestContext(request))

def save_historial(tipo,id_usuario,id_item):
    h=HistorialItem()
    h.fecha_modificacion=timezone_today()
    h.tipo_modificacion=tipo
    h.user_id=id_usuario
    h.item_id=id_item
    h.save()
    

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'HtmlItem/list.html',
        {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )
 
 
 
 
 # Create your views here.
#===============================================================================
def relaciones_item(request,id_proyecto):
     tipoitems=TipoItem.objects.filter(fase__proyecto_id=id_proyecto)
     items=Item.objects.filter(tipo_item__fase__proyecto_id=id_proyecto)
     proyecto=Proyecto.objects.get(pk=id_proyecto)
     buscar=''
     filtro_tipo_id=""
     
     lista_relaciones=Relacion.objects.all()
     items_relaciones=Item.objects.raw('''select distinct i.* from item i
        join relacion r on r.item1_id=i.id or r.item2_id=i.id
        join tipo_item ti on ti.id=i.tipo_item_id
        join fase f on f.id=ti.fase_id
        join proyecto p on p.id=f.proyecto_id
        where p.id='''+str(id_proyecto))
     
     aristas=execute_query('''select distinct r.item1_id,r.item2_id from relacion r 
        join item i on r.item1_id=i.id or r.item2_id=i.id
        join tipo_item ti on ti.id=i.tipo_item_id
        join fase f on f.id=ti.fase_id
        join proyecto p on p.id=f.proyecto_id
        where p.id='''+str(id_proyecto))
     
     
     if request.method == 'GET':
        buscar=request.GET.get('buscar','')
        filtro_tipo_id=request.GET.get('filtro-tipo','')
        
     if request.method == 'POST':
        
        item1=request.POST.get('item1','')
        item2=request.POST.get('item2','')
        descripcion=request.POST.get('descripcion','')
        id_relacion=request.POST.get('id_relacion','')
        print id_relacion, '   ID RELACION    '
        if item1 == '' or item2 == '' or descripcion == '' :
            messages.error(request, "Error al recuperar datos")
            print item1,item2,descripcion
        else:
            if id_relacion == '':
                relacion=Relacion()
                messages.success(request, "Relacion Creada con exito!")
            else:
                relacion=Relacion.objects.get(pk=id_relacion)
                messages.success(request, "Relacion Modificada con exito!")
            relacion.item1_id=item1
            relacion.item2_id=item2
            relacion.tipo=request.POST.get('tipo','')
            relacion.descripcion=descripcion
            relacion.save()
        id_delete=request.POST.get('id_relacion_delete','')
        if id_delete != "":
            Relacion.objects.get(pk=id_delete).delete()
            messages.success(request,"Relacion eliminada correctamente!")
            
            
        
        filtro_tipo_id=request.GET.get('filtro-tipo','')
     
     if filtro_tipo_id != "":
         
         #object_list = Relacion.objects.filter(descripcion__icontains=buscar,Q(item2__tipo_item__fase__proyecto_id=id_proyecto)|Q(item2__tipo_item__fase__proyecto_id=id_proyecto))
         object_list=Relacion.objects.filter(Q(item1__nombre__icontains=buscar)|Q(item2__nombre__icontains=buscar),tipo=filtro_tipo_id)
     else:
         object_list=Relacion.objects.filter(Q(item1__nombre__icontains=buscar)|Q(item2__nombre__icontains=buscar))
         #object_list = Relacion.objects.filter(descripcion__icontains=buscar,Q(item2__tipo_item__fase__proyecto_id=id_proyecto)|Q(item2__tipo_item__fase__proyecto_id=id_proyecto))
     paginator = Paginator(object_list, 10) # Show 25 contacts per page

     page = request.GET.get('page','')
     try:
        page=int(page)
     except:
         page=1    
     try:
         relaciones = paginator.page(page)
     except PageNotAnInteger:
        # If page is not an integer, deliver first page.
         relaciones = paginator.page(1)
     except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        relaciones = paginator.page(paginator.num_pages)

     return render_to_response('HtmlItem/relaciones.html',
    {'tipo_items':tipoitems,'proyecto':proyecto,'items':items,'relaciones':relaciones,'total':object_list.count(),
        'page_range':paginator.page_range,'page':int(page),'buscar':buscar,'placeholder':'Nombre del Item','tipo_relacion':TIPO_RELACION},
                              context_instance=RequestContext(request))