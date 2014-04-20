from django.db import models
from django.contrib.auth.models import User



class Proyecto(models.Model):

    class Meta:
        db_table='proyectos'

    id_proyecto=models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, unique=True)
    leader=models.ForeignKey(User,unique=False)
    fecha_creacion= models.DateTimeField(auto_now=True)
    complejidad=models.IntegerField(default=0)
    estado=models.BooleanField(default=True)
    nro_fases=models.IntegerField()
    coste_total = models.IntegerField()
    descripcion = models.CharField(max_length=300)


from django.db import models
class Rol(models.Model):
    class Meta:
        db_table='roles'

    id_rol=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=30, unique=True)
    descripcion=models.CharField(max_length=300)

