from datetime import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from django.forms.formsets import formset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.dates import timezone_today

from bootstrap_toolkit.widgets import BootstrapUneditableInput
from demo_project.demo_app.models import Rol, Permisos

from .forms import TestForm, TestModelForm, TestInlineForm, WidgetsForm, FormSetInlineForm

#IMPORT FOR RECETARIOS


def demo_form_with_template(request):
    layout = request.GET.get('layout')
    if not layout:
        layout = 'vertical'
    if request.method == 'POST':
        form = TestForm(request.POST)
        form.is_valid()
    else:
        form = TestForm()
    modelform = TestModelForm()
    return render_to_response('form_using_template.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))

def demo_form(request):
    messages.success(request, 'I am a success message.')
    layout = request.GET.get('layout')
    if not layout:
        layout = 'vertical'
    if request.method == 'POST':
        form = TestForm(request.POST)
        form.is_valid()
    else:
        form = TestForm()
    form.fields['title'].widget = BootstrapUneditableInput()
    return render_to_response('form.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))

def demo_form_inline(request):
    layout = request.GET.get('layout', '')
    if layout != 'search':
        layout = 'inline'
    form = TestInlineForm()
    return render_to_response('form_inline.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))

def createAdmin(request):
  cant=User.objects.filter(username='admin').count()
  if cant == 0:
    user=User()
  else:
    user=User.objects.get(username='admin')
  user.username = 'admin'
  user.set_password('admin')
  user.is_staff = True
  user.is_superuser = 'admin'
  user.is_active = True
  user.save()
  return HttpResponseRedirect('/')

def createPermisos(request):
    permiso=Permisos()
    permiso.add_project = True
    permiso.edit_project = True
    permiso.delete_project = True
    permiso.consultar_project = True

    permiso.ver_fase =True

    permiso.add_item = True
    permiso.edit_item = True
    permiso.delete_item = True
    permiso.revive_item = True
    permiso.consultar_item = True
    permiso.relacionar_item =True

    permiso.add_tipo_item = True
    permiso.edit_tipo_item = True
    permiso.delete_tipo_item =True

    permiso.add_rol =True
    permiso.edit_rol = True
    permiso.delete_rol = True
    permiso.asignar_rol = True
    permiso.desasignar_rol =True
    permiso.consultar_rol = True

    permiso.add_user =True
    permiso.edit_user =True
    permiso.delete_user = True
    permiso.consultar_user =True
    permiso.save()
    rol=Rol()
    rol.nombre='admin'
    rol.descripcion='todos los permisos'
    rol.permisos=permiso
    rol.save()
    return HttpResponseRedirect('/')

def demo(request):
    return render_to_response('nicEdit/demos/demo02.html')

def demo_formset(request):
    layout = request.GET.get('layout')
    if not layout:
        layout = 'inline'
    DemoFormSet = formset_factory(FormSetInlineForm)
    if request.method == 'POST':
        formset = DemoFormSet(request.POST, request.FILES)
        formset.is_valid()
    else:
        formset = DemoFormSet()
    return render_to_response('formset.html', RequestContext(request, {
        'formset': formset,
        'layout': layout,
    }))


def demo_tabs(request):
    layout = request.GET.get('layout')
    if not layout:
        layout = 'tabs'
    tabs = [
        {
            'link': "#",
            'title': 'Tab 1',
            },
        {
            'link': "#",
            'title': 'Tab 2',
            }
    ]
    return render_to_response('tabs.html', RequestContext(request, {
        'tabs': tabs,
        'layout': layout,
    }))


def demo_pagination(request):
    lines = []
    for i in range(10000):
        lines.append(u'Line %s' % (i + 1))
    paginator = Paginator(lines, 10)
    page = request.GET.get('page')
    try:
        show_lines = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        show_lines = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        show_lines = paginator.page(paginator.num_pages)
    return render_to_response('pagination.html', RequestContext(request, {
        'lines': show_lines,
    }))


def demo_widgets(request):
    layout = request.GET.get('layout', 'vertical')
    form = WidgetsForm()
    return render_to_response('form.html', RequestContext(request, {
        'form': form,
        'layout': layout,
    }))


