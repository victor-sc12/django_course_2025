from django.urls import path
from . import views

urlpatterns = [
    # path('hola-mundo/', views.index),
    path('', views.index), # El arg 'name' no es necesario especificarlo por el momento
    path('about/', views.about),
    path('contacto/', views.contacto),
    path('portafolio/', views.portafolio),
]