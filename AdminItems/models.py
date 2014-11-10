from django.db import models
from AdminTipoItem.models import TipoItem
from AdminFases.models import Fase
from AdminLineaBase.models import LineaBase
from django.contrib.auth.models import User

# Create your models here.
ESTADOS_ITEM=(('DES','DESARROLLADO'),('APR','APROBADO'),('REV','REVISION'),('ELI','ELIMINADO'),('BLO','BLOQUEADO'))
class Item(models.Model):
    class Meta:
        db_table='item'
    nombre=models.CharField(max_length=50,null=True)
    descripcion=models.CharField(max_length=200,null=True)
    numero=models.IntegerField(null=True)
    tipo_item=models.ForeignKey(TipoItem)
    fase=models.ForeignKey(Fase)
    estado=models.CharField(max_length=50,default='DES')
    propiedad_item=models.IntegerField(null=True)
    linea_base=models.ForeignKey(LineaBase,null=True)
    version = models.IntegerField(null=True)
    complejidad = models.IntegerField(null=True)
    prioridad = models.IntegerField(null=True)

TIPO_MODIFICACION=(('ADD','CREADO'),('EDIT','MODIFICADO'),('DEL','ELIMINADO'),('FIN','FINALIZADO'))
class HistorialItem(models.Model):
    class Meta:
        db_table='historial_item'
    tipo_modificacion=models.CharField(max_length=100,choices=TIPO_MODIFICACION)
    fecha_modificacion=models.DateField()
    user=models.ForeignKey(User)
    item=models.ForeignKey(Item)

