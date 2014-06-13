from django.template.base import Node
from demo_project.demo_app.models import Cambio
from django import template
register=template.Library()

class CambioActual(Node):
    def render(self, context):
        cont_=Cambio.objects.filter(id_cambio=1).count()
        print 'cont: '+str(cont_)
        if cont_ !=0:
            cambio =Cambio.objects.get(pk=1)
        else:
             cambio=Cambio()
             cambio.monto=0
        return cambio.monto

def get_cambio(parser, token):
    return CambioActual()
get_cambio = register.tag(get_cambio)

