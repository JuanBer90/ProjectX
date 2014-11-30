from django.template.base import Node
from django import template
from AdminProyectos.models import Proyecto
register=template.Library()


#===============================================================================
# def get_cambio(parser, token):
#     return CambioActual()
# get_cambio = register.tag(get_cambio)
#===============================================================================
@register.filter
def mis_proyectos(id_user):
    return Proyecto.objects.filter(leader_id=id_user)

@register.filter
def to_str(valor):
    print str(valor)
    return str(valor) 