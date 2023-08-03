from django.contrib import admin #importa el modulo admin de django
from .models import *  #importa todos los modelos



# Register your models here.
admin.site.register(Competencia)
admin.site.register(Temporada)
admin.site.register(Modalidad)
admin.site.register(Deporte)


