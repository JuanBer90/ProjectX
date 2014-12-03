from django.db import models
from AdminTipoItem.models import TipoItem
from AdminFases.models import Fase
from AdminLineaBase.models import LineaBase
from django.contrib.auth.models import User
from django.template.defaultfilters import default

# Create your models here.
ESTADOS_ITEM=(('DES','DESARROLLO'),('APR','APROBADO'),('REV','REVISION'),('ELI','ELIMINADO'),('BLO','BLOQUEADO'))
class Item(models.Model):
    class Meta:
        db_table='item'
    nombre=models.CharField(max_length=50,)#
    descripcion=models.CharField(max_length=300)#
    version = models.IntegerField(default=1)
    padre=models.ForeignKey('Item',null=True)
    tipo_item=models.ForeignKey(TipoItem)#
    prioridad = models.IntegerField(null=True)#
    estado=models.CharField(max_length=50,default='DES',choices=ESTADOS_ITEM)    
    linea_base=models.ForeignKey(LineaBase,null=True)
    costo=models.IntegerField(null=True)#
    complejidad = models.IntegerField(null=True)#
    
    archivos=[]
    
    def __unicode__(self):
        return self.nombre
    
TIPO_RELACION=(('A/S','ANTECESOR/SUCESOR'),('P/H','PADRE/HIJO'))
class Relacion(models.Model):
    class Meta:
        db_table="relacion"
    item1=models.ForeignKey(Item,related_name="item_1")
    item2=models.ForeignKey(Item)
    tipo=models.CharField(max_length=5,choices=TIPO_RELACION)
    descripcion=models.CharField(max_length=200,null=True)
    

TIPO_MODIFICACION=(('ADD','CREADO'),('EDIT','MODIFICADO'),('DEL','ELIMINADO'),('FIN','FINALIZADO'))
class HistorialItem(models.Model):
    class Meta:
        db_table='historial_item'
    tipo_modificacion=models.CharField(max_length=100,choices=TIPO_MODIFICACION)
    fecha_modificacion=models.DateField()
    user=models.ForeignKey(User)
    item=models.ForeignKey(Item)
    
class Document(models.Model):
    class Meta:
        db_table="file"
    item=models.ForeignKey(Item)
    nombre=models.CharField(max_length=50,)
    docfile = models.FileField(upload_to='documents')
