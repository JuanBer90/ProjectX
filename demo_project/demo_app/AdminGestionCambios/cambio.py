from django.shortcuts import render_to_response
from demo_project.demo_app.models import Item
from django.template.context import RequestContext

def cambio(request):
    item_list = Item.objects.filter(estado='BLOQUEADO')
    return render_to_response('HtmlGestionCambio/gestioncambio.html',{'item':item_list}, RequestContext(request))


