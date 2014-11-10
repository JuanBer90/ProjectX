from django.db import models
from AdminFases.models import Fase

# Create your models here.
class TipoItem(models.Model):
    class Meta:
        db_table='tipo_item'
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=300)
    fase=models.ForeignKey(Fase)