from django.db import models


# Create your models here.
class Competencia(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)


    def __str__(self):
        return self.nombre


class Temporada(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=200)
    fechaInicio = models.DateField()
    fechaFin = models.DateField(default=None, null=False, blank=False)
    competencia = models.ForeignKey(Competencia, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.nombre + " - " + self.competencia.nombre
