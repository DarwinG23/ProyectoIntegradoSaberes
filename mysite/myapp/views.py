from django.shortcuts import render
from .forms import *  #importa todos los formularios
from .models import *  #importa todos los modelos
from django.shortcuts import redirect
from django.contrib.auth import login


# Create your views here.
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_superuser = False  # Establece como usuario común
            user.save()
            login(request, user)
            return redirect('nombre_de_la_vista')
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})



def menu(request):
    return render(request, 'menu.html')


def inicioSecion(request):
    return render(request, 'inicioSecion.html')

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
            esPorPuntos =  form.cleaned_data['esPorPuntos']
            cantidadJugadores =  form.cleaned_data['cantidadJugadores']
            puntosLimite =  form.cleaned_data['puntosLimite']
            duracionPartido =  form.cleaned_data['duracionPartido']
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