from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from demo_project.demo_app.constantes import execute_query
from demo_project.demo_app.models import AtributosPorItem, Item, Comite, Proyecto, ComiteUser


def nuevo(request,id):
    comit_to_delete=Comite.objects.filter(proyecto_id=id)
    for co in comit_to_delete:
        co.delete()
    query="select u.* from rol_user ru join auth_user u on u.id = ru.user_id where u.is_active is TRUE and ru.proyecto_id = "+str(id)
    users=User.objects.raw(query)
    proyecto=Proyecto.objects.get(pk=id)
    msg=''

    
    if request.method=='POST':
        cantidad=0
        for user in users:
            check=request.POST.get('check_'+str(user.id),False)
            if check:
                cantidad+=1
        if cantidad%2 != 0 and cantidad > 0:
            comite = Comite()
            comite.nombre = request.POST.get('nombre', '')
            comite.proyecto=proyecto
            comite.save()
            for user in users:
                check=request.POST.get('check_'+str(user.id),False)
                if check:
                    print user.username
                    comite_user=ComiteUser()
                    comite_user.comite=comite
                    comite_user.user=user
                    comite_user.save()
            return HttpResponseRedirect('/comite/ver/'+str(id))
        elif cantidad == 0:
            msg='Seleccione al menos un usuario'
        else:
            msg = 'Ha ingresado un numero impar de usuarios'


    return render_to_response('HtmlComite/nuevo_comite.html',{'users':users,'proyecto':proyecto,'msg':msg}, context_instance=RequestContext(request))

def ver_comite(request,id):
    cant=Comite.objects.filter(proyecto_id=id).count()
    print cant

    if cant == 1:
        comite = execute_query("select c.* from comite c where c.proyecto_id = " + str(id))[0]
        comite_user=ComiteUser.objects.filter(comite_id=comite[0])
    else:
        comite=Comite()
        comite_user=[]
    return render_to_response('HtmlComite/comite.html', {'comite': comite, 'id_proyecto': id,'comite_user':comite_user},
                              context_instance=RequestContext(request))


def editar_comite(request,id):

    query = "select u.* from rol_user ru join auth_user u on u.id = ru.user_id where u.is_active is TRUE and ru.proyecto_id = " + str(id)
    users = User.objects.raw(query)
    proyecto = Proyecto.objects.get(pk=id)
    msg=''
    comite=Comite.objects.get(proyecto_id=id)
    comite_user=ComiteUser.objects.filter(comite=comite)

    if request.method == 'POST':
        cantidad = 0
        for user in users:
            check = request.POST.get('check_' + str(user.id), False)
            if check:
                cantidad += 1
        if cantidad % 2 != 0 and cantidad > 0:
            comite.nombre = request.POST.get('nombre', '')
            comite.proyecto = proyecto
            comite.save()
            for cu in comite_user:
                cu.delete()
            for user in users:
                check = request.POST.get('check_' + str(user.id), False)
                if check:
                    print user.username
                    comite_user = ComiteUser()
                    comite_user.comite = comite
                    comite_user.user = user
                    comite_user.save()
            return HttpResponseRedirect('/comite/ver/' + str(id))
        elif cantidad == 0:
            msg = 'Seleccione al menos un usuario'
        else:
            msg = 'Ha ingresado un numero impar de usuarios'
    if comite_user.__len__() == 0:
        comite.delete()
        comite=Comite()
    return render_to_response('HtmlComite/editar_comite.html',
    {'comite': comite,'msg':msg, 'id_proyecto': id, 'comite_user': comite_user,'users':users,'proyecto':proyecto},
                          context_instance=RequestContext(request))

def eliminar(request,id):
    comite = Comite.objects.get(proyecto_id=id)
    comite_user = ComiteUser.objects.filter(comite=comite)
    for cu in comite_user:
        cu.delete()
    comite.delete()
    return HttpResponseRedirect('/comite/ver/' + str(id))