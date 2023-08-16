from datetime import time, timedelta
from django.contrib.auth.models import User, AbstractUser, Permission, Group
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
    def generar_Partidos(self, deporte, fechaInicio):
        grupos = Grupo.objects.filter(deporte=deporte)

        for grupo in grupos:
            lista_equipos = list(Equipo.objects.filter(grupo=grupo))
            shuffle(lista_equipos)  # Mezclamos los equipos para obtener enfrentamientos aleatorios

            numero_equipos = len(lista_equipos)

            if numero_equipos % 2 != 0:
                lista_equipos.append(None)
                numero_equipos += 1

            partidos_a_crear = []
            fecha_partido = fechaInicio  # Inicializamos la fecha del primer partido

            for i in range(numero_equipos - 1):
                for j in range(i + 1, numero_equipos):
                    equipo_local = lista_equipos[i]
                    equipo_visitante = lista_equipos[j]

                    if equipo_local is None or equipo_visitante is None:
                        # Ignorar los partidos con el equipo "fantasma"
                        continue

                    # Crear el objeto Partido con la fecha y agregarlo a la lista
                    partido = Partido(Grupo=grupo, fecha=fecha_partido, equipo_local=equipo_local,
                                      equipo_visitante=equipo_visitante)
                    partidos_a_crear.append(partido)

                    fecha_partido += timedelta(days=1)  # Incrementar la fecha para el siguiente partido

            # Guardar todos los objetos Partido en la base de datos de una vez
            Partido.objects.bulk_create(partidos_a_crear)

    def generar_horario(self, num_canchas, deporte, hora_inicio, hora_fin):
        # Obtener todos los grupos de la base de datos
        grupos = Grupo.objects.filter(deporte=deporte)

        hora_inicio_entero = hora_inicio.hour
        hora_fin_entero = hora_fin.hour

        diferencia_horas = hora_fin_entero - hora_inicio_entero

        # Crear el objeto Horario y guardarlo en la base de datos
        horario_obj = Horario.objects.create(numCanchas=num_canchas, deporte=deporte, horaInicio=hora_inicio,
                                             horaFin=hora_fin)

        # Recorrer cada grupo y asignar horarios y números de cancha a sus partidos
        for idx, grupo in enumerate(grupos, start=1):
            partidos_grupo = list(grupo.partido_set.all())
            random.shuffle(partidos_grupo)

            # Crear un diccionario para mantener un seguimiento de las canchas disponibles por fecha
            canchas_por_fecha = {}

            # Asignar los partidos a las fechas y canchas disponibles
            for partido in partidos_grupo:
                fecha_asignada = partido.hora

                # Verificar si ya hay canchas asignadas para esa fecha
                if fecha_asignada in canchas_por_fecha:
                    canchas_disponibles = canchas_por_fecha[fecha_asignada]
                else:
                    # Si no hay canchas asignadas para esa fecha, crear una lista de canchas disponibles
                    canchas_disponibles = list(range(1, num_canchas + 1))
                    random.shuffle(canchas_disponibles)
                    canchas_por_fecha[fecha_asignada] = canchas_disponibles

                # Verificar si hay canchas disponibles antes de intentar eliminar una
                if canchas_disponibles:
                    cancha_asignada = canchas_disponibles.pop(0)
                else:
                    cancha_asignada = 1
                    pass

                # Agregar el partido a la fecha y cancha asignada
                partido.cancha = cancha_asignada
                partido.horario = horario_obj

                while hora_inicio_entero <= hora_fin_entero:
                    hora_actual = time(hour=hora_inicio_entero)
                    partidos_misma_fecha_hora = Partido.objects.filter(fecha=fecha_asignada, hora=hora_actual)
                    if len(partidos_misma_fecha_hora) < num_canchas:
                        # Crear objeto time a partir del entero
                        hora_python = time(hora_actual.hour, hora_actual.minute,
                                           hora_actual.second)  # Crear objeto time de Python
                        partido.hora = hora_python
                        break
                    else:
                        hora_inicio_entero += 1
                partido.save()

        for idx, grupo in enumerate(grupos, start=1):
            # Obtener todos los partidos del grupo
              partidos_grupo = list(grupo.partido_set.all())
              for partido in partidos_grupo:
                   fecha_asignada = partido.fecha
                   hora_asignada = partido.hora
                   cancha_asignada = partido.cancha
                   partidos_misma_fecha_hora = Partido.objects.filter(fecha=fecha_asignada, hora=hora_asignada)

                   if len(partidos_misma_fecha_hora) >= num_canchas:
                       partido.hora = time(hora_asignada.hour + 1, hora_asignada.minute, hora_asignada.second)
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


class Competidor(AbstractUser):
    #Atributos
    victorias = models.IntegerField(default=None, null=True, blank=True)
    derrotas = models.IntegerField(default=None, null=True, blank=True)
    empates = models.IntegerField(default=None, null=True, blank=True)
    sancionado = models.BooleanField(default=None, null=True, blank=True)
    partidosJugados = models.IntegerField(default=None, null=True, blank=True)

    # Agrega related_name a las relaciones groups y user_permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='competidores_groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='competidores_user_permissions',
        help_text='Specific permissions for this user.',
    )


    #Relaciones
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, null=True, blank=True)
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'competidor'

    def __str__(self):
        return self.username + " - " + self.equipo.nombre

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
    fecha = models.DateField(verbose_name="Fecha", null=True, blank=True, default=None, unique=False)
    hora = models.TimeField(verbose_name="Hora", null=True, blank=True, default=None, unique=False)
    cancha = models.IntegerField(verbose_name="Numero de cancha", null=True, blank=True)
    marcador_local = models.IntegerField(verbose_name="Marcador local", null=True, blank=True, default='0')
    marcador_visitante = models.IntegerField(verbose_name="Marcador visitante", null=True, blank=True, default='0')

    ESTADO_CHOICES = [
        ('EN JUEGO', 'En juego'),
        ('FINALIZADO', 'Finalizado'),
        ('PENDIENTE', 'Pendiente'),
        ('CANCELADO', 'descnaso'),
        ('DESCANSO', 'descanso'),
        ('APLAZADO', 'aplazado'),
        ('PAUSADO', 'pausado'),
    ]

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

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

class Jugador(models.Model):
    nombre = models.CharField(max_length=100, null=False, unique=True,verbose_name="Nombre")


    #Relaciones
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, null=True, blank=True)
    temporada = models.ForeignKey(Temporada, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        return self.nombre

class Product(models.Model):
    category = models.CharField(max_length=100, null=False, blank=False)
    num_of_products = models.IntegerField()

    def __str__(self):
        return f'{self.category} - {self.num_of_products}'








