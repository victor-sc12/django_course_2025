from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound

# Create your views here.

def index(request): 
    print(request, 'soy una figura')
    return HttpResponse('Hola mundo')

def messages_per_day(request, day): # Imporante que el name del parametro enviado desde la url se ubique igual en la view 
    quotes = {
        'monday' : 'Esta es la quote del lunes',
        'tuesday' : 'Esta es la quote del martes',
        'wednesday' : 'Esta es la quote del miercoles',
        'thursday' : 'Esta es la quote del jueves',
        'friday' : 'Esta es la quote del vierens',
        'saturday' : 'Esta es la quote del sábado',
        'sunday' : 'Esta es la quote del domingo',
        }
    # Lógica implementada sin try-except
        # if day not in quotes.keys():
        #     return HttpResponseNotFound('dia no encontrado')
        # return HttpResponse(quotes[day])
    
    # Lógica implementada con try-except:
    try:
        return HttpResponse(quotes[day])
    except KeyError:
        return HttpResponseNotFound('dia no encontrado')