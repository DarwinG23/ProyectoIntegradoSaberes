from django.urls import path
from . import views


urlpatterns = [
    path('', views.menu, name='menu'),
    path('crearComp/', views.crearComp, name='crearComp'),
    path('crearTemp/', views.crearTemp, name='crearTemp'),
    path('inicioSecion/', views.inicioSecion, name='inicioSecion'),
    path('crearDepo/', views.crearDepo, name='crearDepo'),
    path('registro/', views.registro, name='registro'),
    path('crearEqui/', views.crearEqui, name='crearEqui'),
    path('crearJug/', views.crearCompetidor, name='crearJug'),
    path('crearGrup/', views.crearGrup, name='crearJug'),
    path('crearHorario/', views.crearHorario, name='crearHora'),
    path('Horario/', views.verHorario, name='ver Horario'),

]
