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
    # url(r'^$', 'demo_project.views.home', name='home'),
    # url(r'^demo_project/', include('demo_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^admin$', include(admin.admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name="home"),
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

    #TIPO DE CONTENIDO
    url(r'^contenido/nuevo$', 'demo_app.AdminPermisos.views.nuevo_contenido'),
    url(r'^contenido/editar/(?P<id_contenido>\d+)/$','demo_app.AdminPermisos.views.editar_contenido'),
    url(r'^contenidos/$', 'demo_app.AdminPermisos.views.contenidos'),
    url(r'^permisos/$', 'demo_app.AdminPermisos.views.permisos'),
    url(r'^permiso/editar/(?P<id_permiso>\d+)/$','demo_app.AdminPermisos.views.editar_permiso'),
    url(r'^permiso/nuevo$', 'demo_app.AdminPermisos.views.nuevo_permiso'),


    #PROYECTO
     url(r'^proyecto/nuevo$','demo_app.AdminProyectos.views.nuevo_proyecto'),
     url(r'^proyectos/$', 'demo_app.AdminProyectos.views.proyectos'),
     #url(r'^proyectos/buscar/$', 'demo_app.AdminProyectos.views.buscar_proyectos'),
     url(r'^proyecto/editar/(?P<id_proyecto>\d+)/$','demo_app.AdminProyectos.views.editar_proyecto'),
     url(r'^proyecto/eliminar/(?P<id_proyecto>\d+)/$','demo_app.AdminProyectos.views.eliminar_proyecto'),

     #ROLES
     url(r'^roles/$', 'demo_app.AdminRoles.views.roles'),
     url(r'^rol/nuevo$','demo_app.AdminRoles.views.nuevo_rol'),
     url(r'^rol/editar/(?P<idRol>\d+)/$','demo_app.AdminRoles.views.editar_rol'),
     url(r'^rol/eliminar/(?P<idRol>\d+)/$','demo_app.AdminRoles.views.eliminar_rol'),
)







