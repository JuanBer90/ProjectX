from django.db.models import Q 
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from AdminUsuarios.forms import RegistrationForm, EditUserForm, SinginForm
from django.contrib import messages



def nuevo_usuario(request):
    """
    Crea un nuevo Usuario con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    user=request.user
    if not user.is_superuser:
          return HttpResponseRedirect('/sinpermiso/')

    if request.method=='POST':
        formulario= RegistrationForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return HttpResponseRedirect('/usuarios')
    else:
        formulario= RegistrationForm(request.POST)
    return render_to_response('HtmlUsuarios/nuevousuario.html',{'formulario':formulario}, context_instance=RequestContext(request))


def editar_usuario(request, id_user):
     user=request.user
     if not user.is_superuser:
          return HttpResponseRedirect('/sinpermiso/')
     usuario=User.objects.get(pk=id_user)
     if request.method=='POST':
        formulario =EditUserForm(request.POST,instance=usuario)
        if formulario.is_valid():
            formulario.save()
            messages.success(request,"Usuario Modificado con exito!")
            return HttpResponseRedirect('/usuarios')
        else:
            messages.warning(request,"Debe completar los campos obligatorios!")
     else:
        formulario = EditUserForm(instance=usuario)
     return render_to_response('HtmlUsuarios/editarusuario.html',{'formulario':formulario}, context_instance=RequestContext(request))

def activar_usuario(request, id_user):
    """
    Vuelve activar a un Usuario que anteriomente fue desactivado
    """
    user=request.user
    if not user.is_superuser:
          return HttpResponseRedirect('/sinpermiso/')
    usuario=User.objects.get(pk=id_user)
    usuario.is_active=True
    usuario.save()
    return HttpResponseRedirect('/usuarios')


def ingresar(request):
    """
    Login al Sistema
    """
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/ingresar')
    msg=''
    if request.method == 'POST':
        formulario = SinginForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/home')
                else:
                    return render_to_response('HtmlUsuarios/noactivo.html', context_instance=RequestContext(request))
            else:
               msg='Username y/o password Incorrecto/s'
               messages.error(request,msg)
               return render_to_response('HtmlUsuarios/ingresar.html',{'formulario':formulario }, context_instance=RequestContext(request))
    else:
        formulario = SinginForm()
    return render_to_response('HtmlUsuarios/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def privado(request):
    usuario = request.user
    return render_to_response('HtmlUsuarios/privado.html', {'usuario':usuario}, context_instance=RequestContext(request))



def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')


def usuarios(request):
    buscar=''
    if request.method == 'GET':
        buscar=request.GET.get('buscar','')
    usuarios_list = User.objects.filter(Q(username__icontains=buscar)|Q(first_name__icontains=buscar))
    paginator = Paginator(usuarios_list, 10) # Show 25 contacts per page

    page = request.GET.get('page','')
    try:
        page=int(page)
    except:
        page=1    
    try:
        usuarios = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        usuarios = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        usuarios = paginator.page(paginator.num_pages)

    return render_to_response('HtmlUsuarios/usuarios.html',
                {'objetos':usuarios,'page_range':paginator.page_range,'total':usuarios_list.count(),
                 'page':int(page),'buscar':buscar,'placeholder':'Username o Nombre'
                                                                #'roles':roles
                                                                }, RequestContext(request))

def desactivar_usuario(request,id_user):
    """
    Desactiva al usuario de la lista
    """

    usuario=User.objects.get(pk=id_user)
    usuario.is_active=False
    usuario.save()
    return HttpResponseRedirect('/usuarios')

