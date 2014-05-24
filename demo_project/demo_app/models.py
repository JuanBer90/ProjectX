from django.db import models
from django.contrib.auth.models import User

import constantes



class Proyecto(models.Model):
    """
    Modelo de Proyecto con su respectivo atributos
    """

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

class Permisos(models.Model):
    class Meta:
        db_table='permisos'
    id_permiso=models.AutoField(primary_key=True)
    add_project=models.BooleanField(default=False)
    edit_project=models.BooleanField(default=False)
    delete_project=models.BooleanField(default=False)
    consultar_project=models.BooleanField(default=False)
    ver_fase=models.BooleanField(default=False)
    add_item=models.BooleanField(default=False)
    edit_item=models.BooleanField(default=False)
    delete_item=models.BooleanField(default=False)
    revive_item=models.BooleanField(default=False)
    relacionar_item=models.BooleanField(default=False)
    consultar_item=models.BooleanField(default=False)
    add_tipo_item=models.BooleanField(default=False)
    edit_tipo_item=models.BooleanField(default=False)
    delete_tipo_item=models.BooleanField(default=False)
    add_user=models.BooleanField(default=False)
    edit_user=models.BooleanField(default=False)
    delete_user=models.BooleanField(default=False)
    consultar_user=models.BooleanField(default=False)
    add_rol=models.BooleanField(default=False)
    edit_rol=models.BooleanField(default=False)
    delete_rol=models.BooleanField(default=False)
    asignar_rol=models.BooleanField(default=False)
    desasignar_rol=models.BooleanField(default=False)
    consultar_rol=models.BooleanField(default=False)

class Rol(models.Model):
    class Meta:
        db_table = 'roles'
    id_rol=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=30)
    descripcion=models.CharField(max_length=200)
    permisos=models.ForeignKey(Permisos, unique=False)

class RolUser(models.Model):
    class Meta:
        db_table = 'rol_user'
    id_rol_permiso=models.AutoField(primary_key=True)
    rol=models.ForeignKey(Rol)
    user=models.ForeignKey(User)
    proyecto=models.ForeignKey(Proyecto)



class Fase(models.Model):
    class Meta:
        db_table='fase'
    id_fase= models.AutoField(primary_key=True)
    proyecto=models.ForeignKey(Proyecto)
    posicion=models.IntegerField(null=True)
    nombre = models.CharField(max_length=30, unique=False, null=True)
    numero=models.IntegerField(null=True)
    descripcion = models.CharField(max_length=100,null=True)
    numero_items=models.IntegerField(null=True)
    numero_lb=models.IntegerField(null=True)
    estado=models.CharField(max_length=30,default=constantes.EstadosFase.FASE_NI)
    fecha_creacion= models.DateTimeField(auto_now=True,null=True)

class TipoItem(models.Model):
    class Meta:
        db_table='tipo_item'
    id_tipo_item = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=200)
    proyecto=models.ForeignKey(Proyecto,null=True)
    fase=models.ForeignKey(Fase,null=True)


class LineaBase(models.Model):
    class Meta:
        db_table='linea_base'
    id_linea_base=models.AutoField(primary_key=True)
    numero=models.IntegerField()
    estado=models.CharField(max_length=20,null=True)
    nombre=models.CharField(max_length=50, unique=True)

class Item(models.Model):
    class Meta:
        db_table='item'
    id_item=models.AutoField(primary_key=True)
    nombre=models.eCharField(max_length=30,null=True)
    descripcion=models.CharField(max_length=100,null=True)
    numero=models.IntegerField(null=True)
    tipo_item=models.ForeignKey(TipoItem)
    fase=models.ForeignKey(Fase,null=True)
    estado=models.CharField(max_length=50,default=constantes.EstadosItem.ITEM_NI)
    propiedad_item=models.IntegerField(null=True)
    linea_base=models.ForeignKey(LineaBase,null=True)
    version = models.IntegerField(null=True)
    complejidad = models.IntegerField(null=True)
    prioridad = models.IntegerField(null=True)



class HistorialItem(models.Model):
    class Meta:
        db_table='historial_item'
    id_historial=models.AutoField(primary_key=True)
    tipo_modificacion=models.CharField(max_length=100)
    fecha_modificacion=models.DateField()
    user=models.ForeignKey(User)
    item=models.ForeignKey(Item)


class AtributosPorItem(models.Model):
    class Meta:
        db_table='atributos_por_item'
    id_atributo_por_item=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=32,null=True)
    tipo=models.CharField(max_length=32,null=True)
    valor_defecto=models.CharField(max_length=32,null=True)
    item=models.ForeignKey(Item)


class Relacion(models.Model):
    class Meta:
        db_table='relacion'
    id_relacion=models.AutoField(primary_key=True)
    antes=models.ForeignKey(Item, related_name='antes')
    despues=models.OneToOneField(Item,related_name='despues')
    tipo_relacion=models.CharField(max_length=20)


