from django.conf.app_template import admin
from django.conf.urls import patterns, url, include

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views import static
from django.views.generic import TemplateView
from demo_project import settings

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'demo_project.views.home', name='home'),
    url(r'^$', 'demo_project.demo_app.AdminUsuarios.views.ingresar', name='home'),
    # url(r'^demo_project/', include('demo_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^admin$', include(admin.admin.site.urls)),
    #url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    #url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
    url(r'^contact$', TemplateView.as_view(template_name='contact.html'), name="contact"),
    url(r'^form$', 'demo_app.views.demo_form'),
    url(r'^form_template$', 'demo_app.views.demo_form_with_template'),
    url(r'^form_inline$', 'demo_app.views.demo_form_inline'),
    url(r'^formset$', 'demo_app.views.demo_formset', {}, "formset"),
    url(r'^tabs$', 'demo_app.views.demo_tabs', {}, "tabs"),
    url(r'^pagination$', 'demo_app.views.demo_pagination', {}, "pagination"),
    url(r'^widgets$', 'demo_app.views.demo_widgets', {}, "widgets"),
    url(r'^buttons$', TemplateView.as_view(template_name='buttons.html'), name="buttons"),

    #USUARIOS

    url(r'^ingresar/$','demo_app.AdminUsuarios.views.ingresar'),
    url(r'^privado/$','demo_app.AdminUsuarios.views.privado'),
    url(r'^cerrar/$', 'demo_app.AdminUsuarios.views.cerrar'),
    url(r'^usuario/nuevo$', 'demo_app.AdminUsuarios.views.nuevo_usuario'),
    url(r'^usuarios/$','demo_app.AdminUsuarios.views.usuarios',{},'pagination'),
    url(r'^usuario/eliminar/(?P<id_user>\d+)/$','demo_app.AdminUsuarios.views.desactivar_usuario'),
    url(r'^usuario/activar/(?P<id_user>\d+)/$','demo_app.AdminUsuarios.views.activar_usuario'),
    url(r'^usuario/editar/(?P<id_user>\d+)/$','demo_app.AdminUsuarios.views.editar_usuario'),
    url(r'^demo01/$','demo_app.views.demo'),


    #PROYECTO
     url(r'^proyecto/nuevo$','demo_app.AdminProyectos.views.nuevo_proyecto'),
     url(r'^proyectos/$', 'demo_app.AdminProyectos.views.proyectos'),
     url(r'^proyecto/editar/(?P<id_proyecto>\d+)/$','demo_app.AdminProyectos.views.editar_proyecto'),
     url(r'^proyecto/eliminar/(?P<id_proyecto>\d+)/$','demo_app.AdminProyectos.views.eliminar_proyecto'),

     url(r'^proyecto/misproyectos/$','demo_app.AdminProyectos.views.mis_proyectos'),
     url(r'^proyecto/miproyecto/(?P<id_proyecto>\d+)/$','demo_app.AdminProyectos.views.mi_proyecto'),
     url(r'^proyecto/colaboradores/(?P<id_proyecto>\d+)/$','demo_app.AdminProyectos.views.colaboradores'),



     #ROLES
     url(r'^roles/(?P<id_proyecto>\d+)$', 'demo_app.AdminRoles.views.roles'),
     url(r'^rol/nuevo/(?P<id_proyecto>\d+)/$','demo_app.AdminRoles.views.nuevo_rol'),
     url(r'^rol/editar/(?P<id>\d+)/(?P<id_proyecto>\d+)/$','demo_app.AdminRoles.views.nuevo_rol'),
     # url(r'^rol/eliminar/(?P<idRol>\d+)/$','demo_app.AdminRoles.views.eliminar_rol'),
     url(r'^rol/ver/(?P<idRol>\d+)/(?P<id_proyecto>\d+)/$','demo_app.AdminRoles.views.ver_rol'),
     url(r'^rol/asignar/(?P<id_proyecto>\d+)/$','demo_app.AdminRoles.views.nuevo_rol_user'),
     url(r'^rol/desasignar/(?P<id_rol_user>\d+)/$','demo_app.AdminRoles.views.desasignar_rol'),
     url(r'^sinpermiso/$','demo_app.AdminRoles.views.sinpermiso'),
     url(r'^leader/$','demo_app.AdminRoles.views.nuevo_leader'),

     #FASES
     url(r'^proyecto/fases/(?P<id_proyecto>\d+)$', 'demo_app.AdminFases.views.fases_proyecto'),
     url(r'^fases/crear/(?P<id_fase>\d+)/(?P<id_proyecto>\d+)$', 'demo_app.AdminFases.views.fase'),
     url(r'^fases/edit/(?P<id_fase>\d+)/(?P<id_proyecto>\d+)$', 'demo_app.AdminFases.views.fase'),
     url(r'^fases/import/(?P<id_fase>\d+)/$', 'demo_app.AdminFases.views.importar'),
     url(r'^fases/import/(?P<id_fase>\d+)/(?P<id_import>\d+)$', 'demo_app.AdminFases.views.procesar_import'),



     #TIPO ITEM
     url(r'^tipoitem/nuevo/$','demo_app.AdminTipoItem.views.nuevoTipoItem'),
     url(r'^tipoitem/listar/$','demo_app.AdminTipoItem.views.tipoitem'),
     url(r'^tipoitem/editar/(?P<id_tipoitem>\d+)/$','demo_app.AdminTipoItem.views.editartipoitem'),
     url(r'^tipoitem/eliminar/(?P<id_tipoitem>\d+)/$','demo_app.AdminTipoItem.views.eliminartipoitem'),

    #ITEM
     url(r'^item/nuevo/$','demo_app.AdminItem.views.nuevo_item'),
     url(r'^item/editar/(?P<id>\d+)/$','demo_app.AdminItem.views.editar_item'),
     url(r'^item/eliminar/(?P<id>\d+)/$','demo_app.AdminItem.views.eliminar_item'),
     url(r'^item/listar/$','demo_app.AdminItem.views.listar_items'),

     #Relacion
    url(r'^relacion/nuevo/$','demo_app.AdminRelacion.views.nuevoRelacion'),
    url(r'^relacion/$','demo_app.AdminRelacion.views.relacion'),
    url(r'^relacion/editar/(?P<id>\d+)/$','demo_app.AdminRelacion.views.editarrelacion'),
    url(r'^relacion/eliminar/(?P<id>\d+)/$','demo_app.AdminRelacion.views.eliminarrelacion'),





)







