from django.urls import path
from . import views


urlpatterns = [
    path('crearComp/', views.crearComp, name='crearComp'),
    path('crearTemp/', views.crearTemp, name='crearTemp'),
]
