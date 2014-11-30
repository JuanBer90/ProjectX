from django.shortcuts import render, render_to_response
from AdminFases.models import Fase
from django.template.context import RequestContext
from AdminTipoItem.models import TipoItem
from AdminProyectos.models import Proyecto
from AdminTipoItem.forms import TipoItemForm
from django.contrib import messages
from string import upper

# Create your views here.
#===============================================================================
def tipoitem_proyecto(request,id_proyecto):
     tipoitems=TipoItem.objects.filter(fase__proyecto_id=id_proyecto)
     fases=Fase.objects.filter(proyecto_id=id_proyecto,estado='INI')
     proyecto=Proyecto.objects.get(pk=id_proyecto)
     form=TipoItemForm()
     if request.method == 'POST':
         nombre=request.POST.get('nombre','')
         descripcion=request.POST.get('descripcion','')
         id_tipo=request.POST.get('id_tipo','')
         id_fase=request.POST.get('fase','')
         id_tipo_delete=request.POST.get('id_tipo_delete','')
         
         filtrar= request.POST.get('filtrar','')
         filtro_id_fase=request.POST.get('filtro-fase','')
         if id_fase != '':
             if id_tipo != "":
                 tipo=TipoItem.objects.get(pk=id_tipo)
                 messages.success(request,"Tipo item Editado con exito!")
             else:
                 tipo=TipoItem()
                 messages.success(request,"Tipo item "+upper(tipo.nombre)+" creado!")
             tipo.nombre=nombre
             tipo.fase_id=id_fase
             tipo.descripcion=descripcion
             tipo.save()
         
         if id_tipo_delete != "":
             aux=TipoItem.objects.get(pk=id_tipo_delete)
             messages.error(request,"Tipo item Eliminado "+aux.nombre+" con exito!")
             aux.delete()
         elif filtro_id_fase != "":
             tipoitems=TipoItem.objects.filter(fase_id=filtro_id_fase)
             print "pase por aca"
         
         
     
     return render_to_response('HtmlTipoItem/tipoitemsproyecto.html',
                               {'tipo_items':tipoitems,'proyecto':proyecto,'fases':fases,'form':form},
                              context_instance=RequestContext(request))
