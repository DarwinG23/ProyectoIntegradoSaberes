from django.db.models import Max
from django.shortcuts import render
from .forms import *  #importa todos los formularios
from .models import *  #importa todos los modelos
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from googleapiclient.discovery import build
from django.conf import settings
from googleapiclient.http import MediaFileUpload



# Create your views here.

def menu(request):
    return render(request, 'index.html')



def crearComp(request):
    if request.method == 'GET':
        return render(request, 'crearComp.html', {'form': CompetenciaForm()})
    else:
        form = CompetenciaForm(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            Competencia.objects.create(nombre=nombre, descripcion=descripcion)
        return redirect('crearTemp')

def crearTemp(request):
   if request.method == 'GET':
      return render(request, 'crearTemp.html', {'form': TemporadaForm()})
   else:
      form = TemporadaForm(request.POST)
      if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            fechaInicio = form.cleaned_data['fechaInicio']
            fechaFin = form.cleaned_data['fechaFin']
            competencia = form.cleaned_data['competencia']
            modalidad = form.cleaned_data['modalidad']
            deportes = form.cleaned_data['deportes']
            Temporada.objects.create(nombre=nombre, descripcion=descripcion, fechaInicio=fechaInicio, fechaFin=fechaFin, competencia=competencia, modalidad=modalidad, deportes=deportes)
   return redirect('crearTemp')


def crearDepo(request):
    if request.method == 'GET':
        return render(request, 'crearDepo.html', {'form': DeporteForm()})
    else:
        form = DeporteForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            esPorEquipos = form.cleaned_data['esPorEquipos']
            esPorPuntos = form.cleaned_data['esPorPuntos']
            cantidadJugadores = form.cleaned_data['cantidadJugadores']
            puntosLimite = form.cleaned_data['puntosLimite']
            duracionPartido = form.cleaned_data['duracionPartido']
            cantidadEquipos = form.cleaned_data['cantidadEquipos']
            cantidadTiempos = form.cleaned_data['cantidadTiempos']
            temporada = form.cleaned_data['temporada']
            Deporte.objects.create(nombre=nombre, descripcion=descripcion, esPorEquipos=esPorEquipos, esPorPuntos=esPorPuntos, cantidadJugadores=cantidadJugadores, puntosLimite=puntosLimite, duracionPartido=duracionPartido, cantidadEquipos=cantidadEquipos, cantidadTiempos=cantidadTiempos, temporada=temporada)
        return redirect('crearTemp')


def crearEqui(request):
    if request.method == 'GET':
        return render(request, 'crearEqui.html', {'form': EquipoForm()})
    else:
        form = EquipoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            temporada = form.cleaned_data['temporada']
            deporte = form.cleaned_data['deporte']
            Equipo.objects.create(nombre=nombre, descripcion=descripcion, temporada=temporada, deporte=deporte)
            return redirect('crearEqui')



def crearCompetidor(request):
    if request.method == 'GET':
        return render(request, 'crearCompetidor.html', {'form': CompetidorForm()})
    else:
        form = CompetidorForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            equipo = form.cleaned_data['equipo']
            temporada = form.cleaned_data['temporada']
            Competidor.objects.create(nombre=nombre, equipo=equipo, temporada=temporada)
            return redirect('crearJug')


def crearHorario(request):
    equipos = Equipo.objects.all()
    grupos = Grupo.objects.all()
    fecha = Partido.objects.aggregate(Max('numFecha'))['numFecha__max']
    context = {
        'fecha': fecha,
    }
    if request.method == 'GET':
        return render(request, 'crearHorario.html', {'form': HorarioForm(), 'equipos': equipos, 'grupos': grupos, **context})
    else:
        form = HorarioForm(request.POST)
        if form.is_valid():
            deporte = form.cleaned_data['deporte']
            numCanchas = form.cleaned_data['numCanchas']
            horaInicio = form.cleaned_data['horaInicio']
            horaFin = form.cleaned_data['horaFin']
            grupo = grupos.first()
            grupo.generar_Partidos(deporte)
            grupo.generar_horario(numCanchas, deporte, horaInicio, horaFin)
            return redirect('/Horario')


def crearGrup(request):
    # obtiene los equipos de la base de datos
    equipos = Equipo.objects.all()
    if request.method == 'GET':
        return render(request, 'crearGrup.html', {'form': GrupoForm(), 'equipos': equipos})
    else:
        form = GrupoForm(request.POST)
        if form.is_valid():
            num_grupos = form.cleaned_data['numGrupos']
            deporte = form.cleaned_data['deporte']
            # Generar grupos solo si el número de grupos es mayor a cero
            if num_grupos > 0:
                equipo = equipos.first()
                equipo.generar_Grupos(num_grupos, deporte)
            return redirect('/grupos')

@login_required
def verHorario(request):
    horarios = Horario.objects.all()
    return render(request, 'Horario.html', {'horarios': horarios})


def verEquipos(request):
    equipos = Equipo.objects.all()
    return render(request, 'equipos.html', {'equipos': equipos})

def verCompetidores(request):
    competidores = Competidor.objects.all()
    return render(request, 'competidores.html', {'competidores': competidores})

def verCompetencias(request):
    competencias = Competencia.objects.all()
    temporadas = Temporada.objects.all()
    return render(request, 'competencias.html', {'competencias': competencias, 'temporadas': temporadas})

def salir(request):
    logout(request)
    return redirect('/')

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }
    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('menu')
    return render(request, 'registration/register.html', data)


def verGrupos(request):
    grupos = Grupo.objects.all()
    deportes = Deporte.objects.all()
    return render(request, 'grupos.html', {'grupos': grupos, 'deportes': deportes})

@login_required
def crear(request):
    return render(request, 'crear.html')


def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def sports(request):
    return render(request, 'sports.html')

def news(request):
    # Crear un servicio de la API de YouTube
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

    # Definir el video ID que deseas obtener
    video_id = 'xtHj5fA_5Fg'  # Cambia esto al video ID que quieras

    # Obtener los detalles del video
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    video_info = video_response['items'][0]['snippet']

    return render(request, 'news.html', {'video_info': video_info})

def futbol(request):
    return render(request, 'futbol.html')


def usuario(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user  # Asigna el usuario actual al video
            video.save()
            return redirect('usuario')  # Redirige a la misma página después de cargar el video
    else:
        form = VideoForm()
    return render(request, 'usuario.html', {'form': form})


@login_required
def perfilUsuario(request):
    videos = Video.objects.filter(user=request.user)
    return render(request, 'perfilUsuario.html', {'videos': videos})

