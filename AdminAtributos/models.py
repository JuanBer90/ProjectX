from django.db import models
from django.views.generic.dates import timezone_today
from AdminTipoItem.models import TipoItem

# Create your models here.
TIPO_CHOICES=(('N','Numerico'),('C','Cadena'),('F','Fecha'),
              ('H','Hora'),('L','Logico'),('A','Archivo'))

class Atributo(models.Model):
    class Meta:
        db_table='atributo'
    nombre = models.CharField(max_length=30, unique=True)   
    tipo = models.CharField(max_length=1, choices=(TIPO_CHOICES))
    descripcion = models.TextField(max_length=100, blank=True)
    fecha_creacion = models.DateTimeField(default=timezone_today())
    tipo_item = models.ForeignKey(TipoItem)
    
    numerico=models.IntegerField(null=True)
    logico=models.BooleanField(default=False)
    fecha=models.DateField(null=True)
    archivo=models.FileField(null=True,upload_to='documents/atributos/')
    cadena=models.CharField(null=True,max_length=200)
    hora=models.TimeField(null=True)
    
    def __unicode__(self):
        return self.nombre