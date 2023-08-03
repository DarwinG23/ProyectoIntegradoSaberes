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


class Grupo(models.Model):
    nombre = models.CharField(max_length=50, null=True, unique=True)

    def __str__(self):
        return self.nombre


class Equipo(models.Model):
    #Atributos
    nombre = models.CharField(max_length=100, null=False, unique=True,verbose_name="Nombre")
    descripcion = models.CharField(max_length=200)

    #Relaciones
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, null=True, blank=True)
    grupo = models.ForeignKey(Grupo, on_delete=models.SET_NULL, null = True, blank=True)
    deporte = models.ForeignKey(Deporte, on_delete=models.SET_NULL, null=True, blank=True)

    #Metodos
    def generar_Grupos(self, num_grupos):
        num_equipos = Equipo.objects.count()
        lista_grupos = []

        # Crear los grupos
        for i in range(num_grupos):
            grupo = Grupo.objects.create(nombre="Grupo " + str(i + 1))
            lista_grupos.append(grupo)
            grupo.save()

        self.dividir_equipos( num_grupos, lista_grupos)

    def __str__(self):
        return self.nombre

    def dividir_equipos(self, num_grupos, lista_grupos):
        equipos = Equipo.objects.all()
        for i, equipo in enumerate(equipos):
            grupo_index = i % num_grupos
            lista_grupos[grupo_index].equipo_set.add(equipo)


class Competidor(models.Model):
    #Atributos
    nombre = models.CharField(max_length=100, null=False, unique=False,verbose_name="Nombre")
    victorias = models.IntegerField(default=None, null=True, blank=True)
    derrotas = models.IntegerField(default=None, null=True, blank=True)
    empates = models.IntegerField(default=None, null=True, blank=True)
    sancionado = models.BooleanField(default=None, null=True, blank=True)
    partidosJugados = models.IntegerField(default=None, null=True, blank=True)


    #Relaciones
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, null=True, blank=True)
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nombre + " - " + self.equipo.nombre










