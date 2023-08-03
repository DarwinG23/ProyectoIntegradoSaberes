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
