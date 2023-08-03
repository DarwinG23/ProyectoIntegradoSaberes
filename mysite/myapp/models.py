from django.db import models


# Create your models here.
class Competencia(models.Model):
    #Atributos
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)


    def __str__(self):
        return self.nombre


class Temporada(models.Model):
    #Atributos
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    fechaInicio = models.DateField()
    fechaFin = models.DateField(default=None, null=False, blank=False)

    #Relaciones
    competencia = models.ForeignKey(Competencia, on_delete=models.DO_NOTHING, null=False, blank=False)
    modalidad = models.OneToOneField('Modalidad', on_delete=models.DO_NOTHING, null=False, blank=False, default=None)

    def __str__(self):
        return self.nombre + " - " + self.competencia.nombre


class Modalidad(models.Model):
    #Atributos
    tipoModalidad = models.CharField(max_length=50)

    def __str__(self):
        return self.tipoModalidad



class Deporte(models.Model):
    #Atributos
    nombre = models.CharField(max_length=50, null=False, unique=True)
    descripcion = models.CharField(max_length=200, null=True, blank=True)
    esPorEquipos = models.BooleanField(default=False, null=True, blank=True)
    esPorPuntos = models.BooleanField(default=False, null=True, blank=True)
    cantidadJugadores = models.IntegerField(default=0, null=True, blank=True)
    puntosLimite = models.IntegerField(default=0, null=True, blank=True)
    duracionPartido = models.IntegerField(default=0, null=True, blank=True)
    cantidadEquipos = models.IntegerField(default=0, null=True, blank=True)
    cantidadTiempos = models.IntegerField(default=0, null=False, blank=False)

    #Relaciones
    temporada = models.ForeignKey(Temporada, on_delete=models.DO_NOTHING, null=False, blank=False)

    def __str__(self):
        return self.nombre




