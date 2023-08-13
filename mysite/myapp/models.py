from datetime import time

from django.contrib.auth.models import User
from django.db import models
import random
from random import shuffle





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
    modalidad = models.ForeignKey('Modalidad', on_delete=models.DO_NOTHING, null=False, blank=False, default=None, unique=False)

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


class Grupo (models.Model):
    #Atributos
    nombre = models.CharField(max_length=100, null=True,unique=False,verbose_name="Nombre")


    #Relaciones
    #relacion de una a uno con deporte
    deporte = models.ForeignKey(Deporte, on_delete=models.DO_NOTHING, null=False, blank=False, default=None)

    #Metodos
    def generar_Partidos(self, deporte):

        grupos = Grupo.objects.filter(deporte=deporte)

        for grupo in grupos:
            lista_equipos = list(Equipo.objects.filter(grupo=grupo))
            shuffle(lista_equipos)  # Mezclamos los equipos para obtener enfrentamientos aleatorios

            numero_equipos = len(lista_equipos)

            if numero_equipos % 2 != 0:
                lista_equipos.append(None)
                numero_equipos += 1

            partidos_a_crear = []
            num_fecha = 1  # Inicializamos el número de fecha en 1

            # Crear un diccionario para mantener el contador de fecha para cada equipo
            num_fecha_por_equipo = {equipo: 1 for equipo in lista_equipos}

            for i in range(numero_equipos - 1):
                for j in range(i + 1, numero_equipos):
                    equipo_local = lista_equipos[i]
                    equipo_visitante = lista_equipos[j]

                    if equipo_local is None or equipo_visitante is None:
                        # Ignorar los partidos con el equipo "fantasma"
                        continue

                    # Obtener el número de fecha para cada equipo
                    fecha_local = num_fecha_por_equipo[equipo_local]
                    fecha_visitante = num_fecha_por_equipo[equipo_visitante]

                    # Crear el objeto Partido con el número de fecha y agregarlo a la lista
                    partido = Partido(Grupo=grupo, numFecha=num_fecha, equipo_local=equipo_local,
                                      equipo_visitante=equipo_visitante)
                    partidos_a_crear.append(partido)

                    # Incrementar el contador de fecha para cada equipo
                    num_fecha_por_equipo[equipo_local] += 1
                    num_fecha_por_equipo[equipo_visitante] += 1

                    num_fecha += 1  # Incrementar el número de fecha general
            # Guardar todos los objetos Partido en la base de datos de una vez
            Partido.objects.bulk_create(partidos_a_crear)

    def generar_horario(self, num_canchas, deporte,hora_inicio, hora_fin):
        # Obtener todos los grupos de la base de datos
        grupos = Grupo.objects.filter(deporte=deporte)


        hora_inicio_entero = hora_inicio.hour
        hora_fin_entero = hora_fin.hour

        diferencia_horas = hora_fin_entero - hora_inicio_entero

        # Crear el objeto Horario y guardarlo en la base de datos
        horario_obj = Horario.objects.create(numCanchas=num_canchas, deporte=deporte, horaInicio=hora_inicio, horaFin=hora_fin)

        # Recorrer cada grupo y asignar horarios y números de cancha a sus partidos
        for idx, grupo in enumerate(grupos, start=1):
            partidos_grupo = list(grupo.partido_set.all())
            random.shuffle(partidos_grupo)


            # Crear un diccionario para mantener un seguimiento de las canchas disponibles por fecha
            canchas_por_fecha = {}

            # Asignar los partidos a las fechas y canchas disponibles
            for partido in partidos_grupo:
                fecha_asignada = partido.numFecha


                # Verificar si ya hay canchas asignadas para esa fecha
                if fecha_asignada in canchas_por_fecha:#
                    canchas_disponibles = canchas_por_fecha[fecha_asignada]
                else:
                    # Si no hay canchas asignadas para esa fecha, crear una lista de canchas disponibles
                    canchas_disponibles = list(range(1, num_canchas + 1))
                    random.shuffle(canchas_disponibles)
                    canchas_por_fecha[fecha_asignada] = canchas_disponibles

                # Asignar la primera cancha disponible para el partido en la fecha asignada
                cancha_asignada = canchas_disponibles.pop(0)


                # Agregar el partido a la fecha y cancha asignada
                partido.cancha = cancha_asignada
                partido.horario = horario_obj

                while hora_inicio_entero <= hora_fin_entero:
                    hora_actual = time(hour=hora_inicio_entero)
                    partidos_misma_fecha_hora = Partido.objects.filter(numFecha=fecha_asignada, hora=hora_actual)
                    if len(partidos_misma_fecha_hora) < num_canchas:
                         # Crear objeto time a partir del entero
                        hora_python = time(hora_actual.hour, hora_actual.minute,hora_actual.second)  # Crear objeto time de Python
                        partido.hora = hora_python
                        break
                    else:
                        hora_inicio_entero += 1
                partido.save()

        # Guardar el objeto Horario en la base de datos
        horario_obj.save()



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
    def generar_Grupos(self, num_grupos, deporte):
        num_equipos = Equipo.objects.count()
        lista_grupos = []

        # Crear los grupos
        for i in range(num_grupos):
            grupo = Grupo.objects.create(nombre="Grupo " + str(i + 1), deporte=deporte)
            lista_grupos.append(grupo)
            grupo.save()

        self.dividir_equipos( num_grupos, lista_grupos)

    def __str__(self):
        return self.nombre

    def dividir_equipos(self, num_grupos, lista_grupos):
        equipos = Equipo.objects.all()
        for i, equipo in enumerate(equipos):
            grupo_index = i % num_grupos
            if equipo.deporte == lista_grupos[grupo_index].deporte:
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

class Horario(models.Model):
    # Atributos
    numCanchas = models.IntegerField(verbose_name="Numero de canchas")
    horaInicio = models.TimeField(verbose_name="Hora de inicio", default=None, null=True, blank=True)
    horaFin = models.TimeField(verbose_name="Hora de fin", default=None, null=True, blank=True)

    #Relaciones
    deporte = models.OneToOneField(Deporte, on_delete=models.DO_NOTHING, null=False, blank=False, default=None)

    def __str__(self):
        return " Horario de " + str(self.deporte.nombre)


class Partido(models.Model):
    #Atributos
    numFecha = models.IntegerField(verbose_name="Numero de fecha", null=True, blank=False)
    hora = models.TimeField(verbose_name="Hora", null=True, blank=True, default=None, unique=False)
    cancha = models.IntegerField(verbose_name="Numero de cancha", null=True, blank=True)

    #Relaciones
    Grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE, null=True, blank=True)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, null=True, blank=True)
    equipo_local = models.ForeignKey(Equipo, related_name='partidos_locales', on_delete=models.CASCADE, null=True, blank=True)
    equipo_visitante = models.ForeignKey(Equipo, related_name='partidos_visitantes', on_delete=models.CASCADE, null=True, blank=True)

    #Metodos
    def __str__(self):
        return str(self.equipo_local.nombre) + " vs " + str(self.equipo_visitante.nombre) + " - " + str(self.Grupo.nombre)


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')  # Cambia 'videos/' por la ruta deseada para guardar los videos

    def __str__(self):
        return self.title






