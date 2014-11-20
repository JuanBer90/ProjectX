from django.db import models
from AdminFases.models import Fase

# Create your models here.

ESTADOS_LB=(('INI','INICIADO'),('NOI','NO-INICIADO'),('FIN','FINALIZADO'))
class LineaBase(models.Model):
    class Meta:
        db_table='linea_base'
    id_linea_base=models.AutoField(primary_key=True)
    proyecto=models.ForeignKey(Fase)
    estado=models.CharField(max_length=20,default='INICIADO',choices=ESTADOS_LB)
    numero=models.IntegerField()