from django.urls import path
from . import views


urlpatterns = [
    path('', views.menu, name='menu'),
    path('crearComp/', views.crearComp, name='crearComp'),
    path('crearTemp/', views.crearTemp, name='crearTemp'),
    path('inicioSecion/', views.inicioSecion, name='inicioSecion'),
]
