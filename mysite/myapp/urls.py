from django.urls import path
from . import views


urlpatterns = [
    path('', views.menu, name='menu'),
    path('crearComp/', views.crearComp, name='crearComp'),
    path('crearTemp/', views.crearTemp, name='crearTemp'),
    path('crearDepo/', views.crearDepo, name='crearDepo'),
    path('crearEqui/', views.crearEqui, name='crearEqui'),
    path('crearJug/', views.crearCompetidor, name='crearJug'),
    path('crearGrup/', views.crearGrup, name='crearJug'),
    path('crearHorario/', views.crearHorario, name='crearHora'),
    path('Horario/', views.verHorario, name='ver Horario'),
    path('equipos/', views.verEquipos, name='ver Equipos'),
    path('competidores/', views.verCompetidores, name='ver Competidores'),
    path('competencias/', views.verCompetencias, name='ver Competencias'),
    path('salir/', views.salir, name='salir'),
    path('registro/', views.registro, name='registro'),
    path('grupos/', views.verGrupos, name='ver Grupos'),
    path('crear/', views.crear, name='crear'),
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('calendar', views.calendar, name='calendar'),
    path('news', views.news, name='news'),
    path('sports', views.sports, name='sports'),
    path('futbol', views.futbol, name='futbol'),
]
