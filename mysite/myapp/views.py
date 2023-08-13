import os, json
from django.db.models import Max
from django.shortcuts import render
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from .forms import *  #importa todos los formularios
from .models import *  #importa todos los modelos
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from googleapiclient.discovery import build
from django.conf import settings
from googleapiclient.http import MediaFileUpload
from tempfile import NamedTemporaryFile
import time




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
            Temporada.objects.create(nombre=nombre, descripcion=descripcion, fechaInicio=fechaInicio, fechaFin=fechaFin, competencia=competencia, modalidad=modalidad)
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
    competencias = Competencia.objects.all()
    temporadas = Temporada.objects.all()
    deportes = Deporte.objects.all()
    return render(request, 'Horario.html', {'horarios': horarios, 'competencias': competencias, 'temporadas': temporadas, 'deportes': deportes})


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
    deportes = Deporte.objects.all()

    return render(request, 'sports.html', {'deportes': deportes})

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



def verificarPermiso(request):
    if request.method == 'GET' and 'code' in request.GET:
        secrets_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credenciales', 'YT.json')

        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        flow = Flow.from_client_secrets_file(
            secrets_file_path,
            scopes=['https://www.googleapis.com/auth/youtube.upload'],
            redirect_uri='http://localhost:5000/verificarPermiso'
        )

        flow.fetch_token(authorization_response=request.build_absolute_uri())

        # Guardar las credenciales en un archivo de token
        with open('token.json', 'w') as token_file:
            token_file.write(flow.credentials.to_json())

        return redirect('subirVideo')

    return render(request, 'index.html')


@login_required
def subirVideo(request):
    if request.method == 'POST':
        form = SubirVideoForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtener las credenciales del archivo de token
            with open('token.json', 'r') as token_file:
                token_data = token_file.read()
            credentials = Credentials.from_authorized_user_info(json.loads(token_data))

            youtube = build('youtube', 'v3', credentials=credentials)

            # Detalles del video desde el formulario
            titulo = form.cleaned_data['titulo']
            descripcion = form.cleaned_data['descripcion']
            archivo = form.cleaned_data['archivo']

            # Crear una solicitud de subida de video
            request_body = {
                'snippet': {
                    'title': titulo,
                    'description': descripcion
                },
                'status': {
                    'privacyStatus': 'public'

                }
            }
            # Guardar el archivo temporalmente en el sistema de archivos
            with NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(archivo.read())

            # Subir el archivo de video
            media = MediaFileUpload(temp_file.name, chunksize=-1, resumable=True)
            response = youtube.videos().insert(
                part='snippet,status',
                body=request_body,
                media_body=media
            ).execute()

            # Cierra el archivo temporal
            temp_file.close()

            # Eliminar el archivo temporal después de usarlo
            os.remove(temp_file.name)

            # Marcar el video como no apto para niños
            youtube.videos().update(
                part='status',
                body={'id': response['id'], 'status': {'selfDeclaredMadeForKids': False}}
            ).execute()

            # Redirigir a la página de éxito o a otra vista
            return redirect('perfilUsuario.html')

        else:
            form = SubirVideoForm()

        return render(request, 'subirVideo.html', {'form': form})

    else:
        form = SubirVideoForm()

    return render(request, 'subirVideo.html', {'form': form})



@login_required
def perfilUsuario(request):
    videos = Video.objects.filter(user=request.user)
    return render(request, 'perfilUsuario.html', {'videos': videos})



def autenticar(request):
    secrets_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credenciales', 'YT.json')

    flow = Flow.from_client_secrets_file(
        secrets_file_path,
        scopes=['https://www.googleapis.com/auth/youtube.upload'],
        redirect_uri='http://localhost:5000/verificarPermiso'
    )

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    return redirect(authorization_url)




