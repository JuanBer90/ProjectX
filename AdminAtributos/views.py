from django.shortcuts import render, render_to_response
from AdminFases.models import Fase
from django.template.context import RequestContext
from AdminTipoItem.models import TipoItem
from AdminProyectos.models import Proyecto
from AdminTipoItem.forms import TipoItemForm
from django.contrib import messages
from string import upper
from AdminItems.models import Item, HistorialItem, Document
from AdminItems.forms import ItemForm, UploadFileForm, DocumentForm
from django.views.generic.dates import timezone_today
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from AdminAtributos.models import Atributo, TIPO_CHOICES
from AdminAtributos.forms import AtributoForm


# Create your views here.
#===============================================================================
def atributo_admin(request,id_proyecto):
     tipoitems=TipoItem.objects.filter(fase__proyecto_id=id_proyecto)
     proyecto=Proyecto.objects.get(pk=id_proyecto)
     form=AtributoForm()
     file_form = DocumentForm() # A empty, unbound form
     if request.method == 'POST':
        
         accion=request.POST.get('accion')
         
         if accion =="delete":
             id_delete=request.POST.get("id_delete")
             Atributo.objects.filter(pk=id_delete).delete()
             messages.success(request,message="Atributo eliminado con exito!")
         else:
             if accion == "add":
                 atributo=Atributo()
                 messages.success(request,message="Atributo "+upper(atributo.nombre)+" creado con exito!")
             if accion=="edit":
                 id_atributo=request.POST.get("id_edit")
                 if id_atributo != "":
                     atributo=Atributo.objects.get(pk=id_atributo)
                     messages.success(request,message="Atributo modificado con exito!")
                 else:
                     messages.error(request,message="No se pudo editar el atributo!")
             tipo=request.POST.get('tipo_atr','')
             print "TIPO: ",tipo,"  ",request.POST.get('hora')
             if tipo =="H":
                 atributo.hora=request.POST.get('hora')
             if tipo == "C":
                 atributo.cadena=request.POST.get('cadena')
             if tipo == "numerico":
                 atributo.numerico=request.POST.get('numerico')
             if tipo == "F":
                 atributo.fecha=request.POST.get('fecha')
             if tipo == "L":
                 logic=request.POST.get('logico')
                 if logic != "":
                     atributo.logico=True
                 else:
                     atributo.logico=False
             if tipo =="A":
                 #==============================================================
                 # newdoc = Document(docfile = )
                 # atributo_file=request.POST.get('id_atributo_file','')
                 # if atributo_file != "":
                 #   newdoc.nombre=request.POST.get('nombre_archivo','')
                 #   newdoc.save()
                 #==============================================================
                 atributo.archivo=request.FILES.get('archivo','')
                     
             atributo.tipo=tipo
             atributo.nombre=request.POST.get('nombre','')
             atributo.descripcion=request.POST.get('descripcion','')
             atributo.tipo_item_id=request.POST.get('tipo_item','')
             atributo.save()
             
         return HttpResponseRedirect("/proyecto/atributos/"+str(id_proyecto))
     buscar=''
     filtro_tipo_id=""
     if request.method == 'GET':
        buscar=request.GET.get('buscar','')
        filtro_tipo_id=request.GET.get('filtro-tipo','')
     
     if filtro_tipo_id != "":
         atributos_list = Atributo.objects.filter(nombre__icontains=buscar,tipo_item_id=filtro_tipo_id,tipo_item__fase__proyecto_id=id_proyecto)
     else:
         atributos_list = Atributo.objects.filter(nombre__icontains=buscar,tipo_item__fase__proyecto_id=id_proyecto)
    
     paginator = Paginator(atributos_list, 10) # Show 25 contacts per page
     page = request.GET.get('page','')
     try:
        page=int(page)
     except:
         page=1    
     try:
         atributos = paginator.page(page)
     except PageNotAnInteger:
        # If page is not an integer, deliver first page.
         atributos = paginator.page(1)
     except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        atributos = paginator.page(paginator.num_pages)
     for a in atributos:
         print a.nombre,"   ",a.tipo
     return render_to_response('HtmlAtributo/atributos_tipoitem.html',
    {'tipo_items':tipoitems,'proyecto':proyecto,'atributos':atributos,'tipo_atributo':TIPO_CHOICES,'total':atributos_list.count(),
        'file_form':file_form,'form':form,'page_range':paginator.page_range,'page':int(page),'buscar':buscar,'placeholder':'Nombre'},
                              context_instance=RequestContext(request))

def save_historial(tipo,id_usuario,id_item):
    h=HistorialItem()
    h.fecha_modificacion=timezone_today()
    h.tipo_modificacion=tipo
    h.user_id=id_usuario
    h.item_id=id_item
    h.save()
    
