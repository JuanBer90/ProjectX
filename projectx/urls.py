from django.conf.app_template import admin
from django.conf.urls import patterns, url, include

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views import static
from django.views.generic import TemplateView
from dajaxice.core.Dajaxice import dajaxice_autodiscover
from dajaxice.core import dajaxice_config

dajaxice_autodiscover()
urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'demo_project.views.home', name='home'),
    
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^$', 'AdminUsuarios.views.ingresar', name='home'),
    url(r'^admin$', include(admin.admin.site.urls)),
    #url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    #===========================================================================
    # url(r'^contact$', TemplateView.as_view(template_name='contact.html'), name="contact"),
    # url(r'^form$', '.demo_form'),
    # url(r'^form_template$', 'views.demo_form_with_template'),
    # url(r'^form_inline$', 'views.demo_form_inline'),
    # url(r'^formset$', 'views.demo_formset', {}, "formset"),
    # url(r'^tabs$', 'views.demo_tabs', {}, "tabs"),
    # url(r'^pagination$', 'views.demo_pagination', {}, "pagination"),
    # url(r'^widgets$', 'views.demo_widgets', {}, "widgets"),
    # url(r'^buttons$', TemplateView.as_view(template_name='buttons.html'), name="buttons"),
    #===========================================================================

    #USUARIOS

    url(r'^ingresar/$','AdminUsuarios.views.ingresar'),
    url(r'^home/$',TemplateView.as_view(template_name="index.html"),name='home'),
    url(r'^cerrar/$', 'AdminUsuarios.views.cerrar'),
    url(r'^usuario/nuevo$', 'AdminUsuarios.views.nuevo_usuario'),
    url(r'^usuarios/$','AdminUsuarios.views.usuarios',{},'pagination'),
    url(r'^usuario/eliminar/(?P<id_user>\d+)/$','AdminUsuarios.views.desactivar_usuario'),
    url(r'^usuario/activar/(?P<id_user>\d+)/$','AdminUsuarios.views.activar_usuario'),
    url(r'^usuario/editar/(?P<id_user>\d+)/$','AdminUsuarios.views.editar_usuario'),
    #url(r'^demo01/$','views.demo'),
   # url(r'^create_admin/$', 'views.createAdmin'),
    #url(r'^create_rol_admin/$', 'views.createPermisos'),




    #PROYECTO
     url(r'^proyecto/nuevo$','AdminProyectos.views.nuevo_proyecto'),
     url(r'^proyectos/$', 'AdminProyectos.views.proyectos'),
     url(r'^proyecto/editar/(?P<id_proyecto>\d+)/$','AdminProyectos.views.editar_proyecto'),
     url(r'^proyecto/iniciar/(?P<id_proyecto>\d+)/$','AdminProyectos.views.iniciar_proyecto'),
     url(r'^proyecto/eliminar/(?P<id_proyecto>\d+)/$','AdminProyectos.views.eliminar_proyecto'),
     url(r'^proyecto/misproyectos/$','AdminProyectos.views.mis_proyectos'),
     url(r'^proyecto/miproyecto/(?P<id_proyecto>\d+)/$','AdminProyectos.views.mi_proyecto'),
     url(r'^proyecto/colaboradores/(?P<id_proyecto>\d+)/$','AdminProyectos.views.colaboradores'),
     
     url(r'^proyecto/tipoitem/(?P<id_proyecto>\d+)/$','AdminTipoItem.views.tipoitem_proyecto'),
     url(r'^proyecto/items/(?P<id_proyecto>\d+)/$','AdminItems.views.items_proyecto'),
     
     #url(r'^proyecto/items/(?P<id>\d+)/$', 'AdminItem.views.item_proyecto'),
     #url(r'^proyecto/relaciones/(?P<id>\d+)/$', 'AdminRelacion.views.relacion_proyecto'),
     #url(r'^proyecto/relacion_delete/(?P<id>\d+)/(?P<id_proyecto>\d+)/$', 'AdminRelacion.views.eliminarrelacion'),
     #url(r'^proyecto/aprobar/(?P<id>\d+)/$', 'AdminItem.views.aprobar_principal'),

     #==========================================================================
     # #ROLES
     # url(r'^roles/(?P<id_proyecto>\d+)$', 'AdminRoles.views.roles'),
     # url(r'^rol/nuevo/(?P<id_proyecto>\d+)/$','AdminRoles.views.nuevo_rol'),
     # url(r'^rol/editar/(?P<id>\d+)/(?P<id_proyecto>\d+)/$','AdminRoles.views.nuevo_rol'),
     # # url(r'^rol/eliminar/(?P<idRol>\d+)/$','AdminRoles.views.eliminar_rol'),
     # url(r'^rol/ver/(?P<idRol>\d+)/(?P<id_proyecto>\d+)/$','AdminRoles.views.ver_rol'),
     # url(r'^rol/asignar/(?P<id_proyecto>\d+)/$','AdminRoles.views.nuevo_rol_user'),
     # url(r'^rol/desasignar/(?P<id_rol_user>\d+)/$','AdminRoles.views.desasignar_rol'),
     # url(r'^sinpermiso/$','AdminRoles.views.sinpermiso'),
     # url(r'^leader/$','AdminRoles.views.nuevo_leader'),
     # url(r'^default_leader/$', 'createUser.create_rol'),
     #==========================================================================


     #FASES
     url(r'^proyecto/fases/(?P<id_proyecto>\d+)$', 'AdminFases.views.fases_proyecto'),
     
     url(r'^fases/crear/(?P<id_fase>\d+)/(?P<id_proyecto>\d+)$', 'AdminFases.views.fase'),
     url(r'^fases/cerrar/(?P<id>\d+)/$', 'AdminFases.views.cerrar'),
     url(r'^fases/edit/(?P<id_fase>\d+)/(?P<id_proyecto>\d+)$', 'AdminFases.views.fase'),
     url(r'^fases/import/(?P<id_fase>\d+)/$', 'AdminFases.views.importar'),
     #url(r'^fases/import/(?P<id_fase>\d+)/(?P<id_import>\d+)$', 'AdminFases.views.procesar_import'),
     #==========================================================================
     # url(r'^fases/tipoitems/(?P<id>\d+)$', 'AdminFases.views.fase_tipo_item'),
     #==========================================================================
     #url(r'^fases/tipoitems/add/(?P<id>\d+)$', 'AdminTipoItem.views.TipoItemToFase'),



      #TIPO ITEM
      #=========================================================================
      # url(r'^proyecto/tipoitem/(?P<id_proyecto>\d+)$', 'AdminFases.views.fases_proyecto'),
      #=========================================================================
#      url(r'^tipoitem/nuevo/$','AdminTipoItem.views.nuevoTipoItem'),
#      url(r'^tipoitem/listar/$','AdminTipoItem.views.tipoitem'),
#      url(r'^tipoitem/editar/(?P<id_tipoitem>\d+)/$','AdminTipoItem.views.editartipoitem'),
#      url(r'^tipoitem/eliminar/(?P<id_tipoitem>\d+)/$','AdminTipoItem.views.eliminartipoitem'),
#      url(r'^tipoitem/items/(?P<id>\d+)/$','AdminTipoItem.views.TipoItemToItem'),
#      url(r'^tipoitem/items/add/(?P<id>\d+)/$','AdminItem.views.TipoItem_nuevo_item'),
#      url(r'^tipoitem/items/edit/(?P<id>\d+)/$','AdminItem.views.TipoItem_editar_item'),
#===============================================================================
    #ITEM
#===============================================================================
#      url(r'^item/nuevo/$','AdminItem.views.nuevo_item'),
#      url(r'^item/editar/(?P<id>\d+)/$','AdminItem.views.editar_item'),
#      url(r'^item/eliminar/(?P<id>\d+)/$','AdminItem.views.eliminar_item'),
#      url(r'^item/listar/$','AdminItem.views.listar_items'),
#      url(r'^item/historial/(?P<id>\d+)/$','AdminItem.views.historial'),
#      url(r'^item/aprobar/(?P<id>\d+)/$','AdminItem.views.aprobar'),
#      url(r'^item/upload/$', 'AdminItem.views.upload'),
#      url(r'^item/revivir/(?P<id>\d+)/$', 'AdminItem.views.revivir_item'),
#      url(r'^item/finalizar/(?P<id>\d+)/$', 'AdminItem.views.finalizar'),
#      url(r'^item/add_lb/(?P<id>\d+)/$', 'AdminItem.views.add_lb'),
# 
#     #RELACION
#     url(r'^relacion/nuevo/$','AdminRelacion.views.nuevoRelacion'),
#     url(r'^relacion/$','AdminRelacion.views.relacion'),
#     url(r'^relacion/editar/(?P<id>\d+)/$','AdminRelacion.views.editarrelacion'),
#     url(r'^relacion/eliminar/(?P<id>\d+)/$','AdminRelacion.views.eliminarrelacion'),
#     url(r'^relacion/items/(?P<id>\d+)/$','AdminRelacion.views.relacion_item'),
#     url(r'^relacion/items/(?P<id>\d+)/(?P<tipo>\d+)/(?P<antes>\d+)$', 'AdminRelacion.views.'),
#     url(r'^relacion/padre_hijo/(?P<id>\d+)/', 'AdminRelacion.views.padre_hijo'),
#     url(r'^relacion/antecesor/(?P<id>\d+)/', 'AdminItem.views.antec_suc'),
# 
# 
#     #AtributoItem
#     url(r'^atributoitem/nuevo/$','AdminAtributosItem.views.nuevoatributoitem'),
#     url(r'^atributoitem/$','AdminAtributosItem.views.atributoitem'),
#     url(r'^atributoitem/editar/(?P<id>\d+)/$','AdminAtributosItem.views.editaratributoitem'),
#     url(r'^atributoitem/eliminar/(?P<id>\d+)/$','AdminAtributosItem.views.eliminaratributoitem'),
#     url(r'^atributoitem/atributos/(?P<id>\d+)/$','AdminAtributosItem.views.atributos_por_item'),
#     url(r'^atributoitem/atributos/atributo/(?P<id>\d+)/$','AdminAtributosItem.views.ver_atributo'),
#     url(r'^atributoitem/add_atributo_item/(?P<id>\d+)/$','AdminAtributosItem.views.add_atributo_item'),
#     url(r'^atributoitem/edit_atributo_item/(?P<id>\d+)/$','AdminAtributosItem.views.edit_atributo_item'),
#     url(r'^atributoitem/delete_atributo_item/(?P<id>\d+)/$','AdminAtributosItem.views.delete_atributo_item'),
#===============================================================================

    #LineaBase
#===============================================================================
#     url(r'^lineabase/nuevo/(?P<id>\d+)/$','AdminLineaBase.views.nuevo_lb'),
#     url(r'^lineabase/editar/(?P<id>\d+)/$', 'AdminLineaBase.views.editar_lb'),
#     url(r'^lineabase/cerrar/(?P<id>\d+)/$', 'AdminLineaBase.views.cerrar'),
#     url(r'^lineabase/listar/(?P<id>\d+)/$', 'AdminLineaBase.views.listar_lb'),
#     url(r'^lineabase/items/(?P<id>\d+)/$', 'AdminLineaBase.views.items'),
#     url(r'^lineabase/add_item/(?P<id_item>\d+)/(?P<id_lb>\d+)$', 'AdminLineaBase.views.item_to_lb'),
# 
#     #COMITE
#     url(r'^comite/nuevo/(?P<id>\d+)/$', 'AdminComite.views.nuevo'),
#     url(r'^comite/ver/(?P<id>\d+)/$', 'AdminComite.views.ver_comite'),
#     url(r'^comite/editar/(?P<id>\d+)/$', 'AdminComite.views.editar_comite'),
#     url(r'^comite/eliminar/(?P<id>\d+)/$', 'AdminComite.views.eliminar'),
# 
#     url(r'^item/reporte/(?P<id>\d+)/$', 'AdminItem.views.item_reporte'),
#     url(r'^lineabase/reporte/(?P<id>\d+)/$', 'AdminLineaBase.views.lb_reporte'),
# 
#     url(r'^lineabase/historial/(?P<id>\d+)/$', 'AdminLineaBase.views.historial')
#===============================================================================



)







