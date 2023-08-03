import django.forms as forms
from .models import *




class CompetenciaForm( forms.Form ):
    nombre = forms.CharField( label='Nombre', max_length=50 )
    descripcion = forms.CharField( label='Descripcion', max_length=200)

class TemporadaForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100, required=True)
    descripcion = forms.CharField(label="Descripcion", max_length=200, required=False)
    fechaInicio = forms.DateField(label="Fecha de inicio", required=True)
    fechaFin = forms.DateField(label="Fecha de fin", required=True)
    competencia = forms.ModelChoiceField(queryset=Competencia.objects.all(), empty_label=None, label="Competencia")
    modalidad = forms.ModelChoiceField(queryset=Modalidad.objects.all(), empty_label=None, label="Modalidad")
    deportes = forms.ModelMultipleChoiceField(queryset=Deporte.objects.all(), label="Deportes", required=False)

class DeporteForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=50, required=True)
    descripcion = forms.CharField(label="Descripcion", max_length=200, required=False)
    esPorEquipos = forms.BooleanField(label="Es por equipos", required=False)
    esPorPuntos = forms.BooleanField(label="Es por puntos", required=False)
    cantidadJugadores = forms.IntegerField(label="Cantidad de jugadores", required=False)
    puntosLimite = forms.IntegerField(label="Puntos limite", required=False)
    duracionPartido = forms.IntegerField(label="Duracion del partido", required=False)
    cantidadEquipos = forms.IntegerField(label="Cantidad de equipos", required=False)
    cantidadTiempos = forms.IntegerField(label="Cantidad de tiempos", required=False)
    temporada = forms.ModelChoiceField(queryset=Temporada.objects.all(), empty_label=None, label="Temporada")
