from django.db.models import Q 
from django.contrib.auth.hashers  import make_password
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
from AdminProyectos.models import Proyecto
from AdminUsuarios.models import Miembro
from AdminUsuarios.send_email import  *


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
            usuario=formulario.save(commit=False)
            password=request.POST.get("password1",'')
            SendMail(password=password,username=usuario.username,correo=usuario.email)
            messages.success(request,"Usuario creado satisfactoriamente!")
            messages.info(request,"Mensaje de Bienvenida enviado al usuario!")
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
        return HttpResponseRedirect('/home')
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


def miembros(request,id_proyecto):
    proyecto=Proyecto.objects.get(pk=id_proyecto)
    buscar=''
    if request.method == 'GET':
        buscar=request.GET.get('buscar','')
    usuarios_list = Miembro.objects.filter(Q(usuario__username__icontains=buscar)|Q(usuario__first_name__icontains=buscar),proyecto_id=id_proyecto)
    paginator = Paginator(usuarios_list, 10) # Show 25 contacts per page
    no_miembros=Miembro.objects.raw('''select * from auth_user EXCEPT select u.* from miembros m 
        join auth_user u on u.id=m.usuario_id where m.proyecto_id='''+str(id_proyecto))
    
    if request.method == 'POST':
        id_usuario= request.POST.get('id_miembro','')
        id_user_delete=request.POST.get('id_miembro_delete','')
        if id_usuario != '':
            miembro=Miembro()
            miembro.usuario_id=id_usuario
            miembro.proyecto_id=id_proyecto
            miembro.save()
            messages.success(request,"Usuario agregado satisfactoriamente!")
        if id_user_delete != '':
            Miembro.objects.get(pk=id_user_delete).delete()
            messages.success(request,"Usuario Eliminado satisfactoriamente!")
    
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

    return render_to_response('HtmlUsuarios/miembrosproyecto.html',
                {'objetos':usuarios,'page_range':paginator.page_range,'total':usuarios_list.count(),
                 'page':int(page),'no_miembros':no_miembros,'proyecto':proyecto,'buscar':buscar,'placeholder':'Username o Nombre'
                                                                #'roles':roles
                                                             }, RequestContext(request))

def recuperar(request):
    if request.method=="POST":
        username=request.POST.get("username","")
        if User.objects.filter(username=username).exists():
            user=User.objects.get(username=username)
            email=user.email
            id_usuario=user.id
            return HttpResponseRedirect('/reestablecer/'+str(id_usuario)+'/?correo='+email)
            
        else:
            messages.warning(request,"Usuario "+username+" no existe!")
    
    return render_to_response('HtmlUsuarios/recuperar.html', {}, context_instance=RequestContext(request))


def reestablecer_pass(request,id_user):
    nuevo_pass= GenPasswd(5).upper()
    usuario=User.objects.get(pk=id_user)
    usuario.password=make_password(nuevo_pass)
    usuario.save()
    correo=request.GET.get("correo",'')
    if correo !="":
        SendPassword(password=nuevo_pass,username=request.user.username,correo=correo)
        messages.success(request,"Password restablecido correctamente! Verifique su correo!")
        return HttpResponseRedirect("/")
    else:
        messages.error(request,"Ha ocurrido un error, ingrese de vuelta su usuario!")
        return HttpResponseRedirect('/recuperar/')

import string
from random import choice

def GenPasswd(n):
    return ''.join([choice(string.letters + string.digits) for i in range(n)])


