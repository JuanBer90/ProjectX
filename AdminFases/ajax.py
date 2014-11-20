from datetime import datetime
from django.db.models.sql.datastructures import Date
from django.template.defaultfilters import time
from django.utils import simplejson
from dajaxice.decorators import dajaxice_register
from django.views.generic.dates import timezone_today
import json
from AdminFases.models import Fase
@dajaxice_register
def sayhello(request):
    print "asdfasdfsadf"
    
    return json.dumps({'message':'Hello World'})


@dajaxice_register
def search_fases(request, buscar):
    print "ASDFADSFASDF"
    fases=Fase.objects.filter(nombre__icontains=buscar)
    datos=[]
    for fase in fases:
        dato={'id':fase.id,
              'nombre':fase.nombre,
              'estado':fase.estado
              }
        datos.append(dato)
    return simplejson.dumps(datos)
