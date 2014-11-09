from django.db import models
from AdminProyectos.models import Proyecto

ESTADOS_FASE=(('INI','INICIADO'),('NOI','NO-INICIADO'),('FIN','FINALIZADO'))

class Fase(models.Model):
    class Meta:
        db_table='fase'
    proyecto=models.ForeignKey(Proyecto)
    posicion=models.IntegerField(null=True)
    nombre = models.CharField(max_length=30, unique=False, null=True)
    numero=models.IntegerField(null=True)
    descripcion = models.CharField(max_length=100,null=True)
    numero_items=models.IntegerField(null=True)
    numero_lb=models.IntegerField(null=True)
    estado=models.CharField(max_length=30,default='NOI')
    fecha_creacion= models.DateTimeField(auto_now=True,null=True)
