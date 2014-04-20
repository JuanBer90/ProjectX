#from django.db import models
#from django.contrib.auth.models import User



#class Proyecto(models.Model):

#    class Meta:
#        db_table='proyectos'

#    id_proyecto=models.AutoField(primary_key=True)
#    leader=models.OneToOneField(User, primary_key=True)
#    nombre = models.CharField(max_length=30, unique=True)
#    descripcion= models.TextField(max_length=300, help_text='Descripcion del Proyecto')
#    fecha_creacion= models.DateTimeField(auto_created=True)
#    complejidad=models.IntegerField(default=0)
#    estado=models.BooleanField(default=True)
#    nro_fases=models.IntegerField()
#    coste_total = models.IntegerField()
