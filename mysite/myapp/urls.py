from django.urls import path
from . import views
from .views import CatalogoView, mostrar_catalogo

urlpatterns = [
    path('', views.menu, name='menu'),
]
