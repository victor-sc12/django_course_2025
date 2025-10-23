from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    
    # URLS Dinámicas:
    # se envia el arg 'day' a la vista como parametro
    # se puede dejar el arg con su nombre, o declarar el tipo de dato al que pertenece. Por ejm: <str:arg>, <int:arg>, etc
    path('<int:day>/', views.messages_per_day_with_number),
    path('<str:day>/', views.messages_per_day, name='message_x_day'),
]