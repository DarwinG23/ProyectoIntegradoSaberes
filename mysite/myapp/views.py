from django.shortcuts import render
from .forms import CompetenciaForm
from .models import Competencia
from django.shortcuts import redirect

# Create your views here.
def menu(request):
    if request.method == 'GET':
       return render(request, 'menu.html', {'form': CompetenciaForm()})
    else:
        form = CompetenciaForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            Competencia.objects.create(nombre=nombre, descripcion=descripcion)
            return redirect('/')
