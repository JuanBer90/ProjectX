
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from demo_project.demo_app import constantes
from demo_project.demo_app.AdminUsuarios.forms import RegistrationForm, EditUserForm
from demo_project.demo_app.models import RolUser


def nuevo_usuario(request):
    """
    Crea un nuevo Usuario con sus atributos proveidos por el
    usuario y el Sistema autogenera los demas atributos
    """
    user=request.user
    print 'SUPER USUARIO? :'+str(user.is_superuser)+'\n Username: '+user.username
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
            return HttpResponseRedirect('/usuarios')
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
        return HttpResponseRedirect('/privado')
    msg=''
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request, acceso)
                    return HttpResponseRedirect('/privado')
                else:
                    return render_to_response('HtmlUsuarios/noactivo.html', context_instance=RequestContext(request))
            else:
               msg='Username y/o password Incorrecto/s'
               return render_to_response('HtmlUsuarios/ingresar.html',{'formulario':formulario ,'msg':msg}, context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('HtmlUsuarios/ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def privado(request):
    usuario = request.user
    return render_to_response('HtmlUsuarios/privado.html', {'usuario':usuario}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def cerrar(request):
    logout(request)
    return HttpResponseRedirect('/')


def usuarios(request):
    """
    Lista de a 10 a los usuarios por pagina
    """
    user=request.user
    if not user.is_superuser:
          return HttpResponseRedirect('/sinpermiso/')
    nro_lineas=10
    lines = []

    page = request.GET.get('page')
    usuarios_total = User.objects.count()
    for i in range(usuarios_total):
        lines.append(u'Line %s' % (i + 1))

    paginator = Paginator(lines, nro_lineas)
    try:
        page=int(page)
    except:
        page=1

    if int(page)*nro_lineas>usuarios_total or int(page)>0:
        try:
            users = paginator.page(page)
            fin=int(page)*nro_lineas
            ini =fin-nro_lineas
        except PageNotAnInteger or EmptyPage:
            fin=nro_lineas
            ini=0
            users = paginator.page(1)
    else:
        fin=nro_lineas
        ini=0
        users = paginator.page(1)


    usuarios_list = User.objects.order_by('username').all()[ini:fin]
    roles=RolUser.objects.all()
    # for r in roles:
    #     print r.rol.descripcion
    #     print r.user.username
    return render_to_response('HtmlUsuarios/usuarios.html',{'usuarios':usuarios_list, 'roles':roles}, RequestContext(request, {
        'lines': users
    }))

def desactivar_usuario(request,id_user):
    """
    Desactiva al usuario de la lista
    """

    usuario=User.objects.get(pk=id_user)
    usuario.is_active=False
    usuario.save()
    return HttpResponseRedirect('/usuarios')

