from django.db import models
from django.contrib.auth.models import User

ESTADOS_PROYECTO=(('INI','INICIADO'),('NOI','NO-INICIADO'),('FIN','FINALIZADO'))
   

class Proyecto(models.Model):
    """
    Modelo de Proyecto con su respectivo atributos
    """
    class Meta:
        db_table='proyecto'

    nombre = models.CharField(max_length=30, unique=True)
    leader=models.ForeignKey(User,unique=False)
    fecha_creacion= models.DateTimeField(auto_now=True)
    complejidad=models.IntegerField(default=0)
    estado=models.CharField(choices=ESTADOS_PROYECTO,default='NOI',max_length=30)
    nro_fases=models.IntegerField()
    coste_total = models.IntegerField()
    descripcion = models.CharField(max_length=300)