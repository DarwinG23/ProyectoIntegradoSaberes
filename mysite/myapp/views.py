from django.shortcuts import render
from .forms import *  #importa todos los formularios
from .models import *  #importa todos los modelos
from django.shortcuts import redirect

# Create your views here.
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
            Temporada.objects.create(nombre=nombre, descripcion=descripcion, fechaInicio=fechaInicio, fechaFin=fechaFin, competencia=competencia)
   return redirect('crearTemp')



