from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse

# Dict to quotes:
quotes = {
        'monday' : 'Esta es la quote del lunes',
        'tuesday' : 'Esta es la quote del martes',
        'wednesday' : 'Esta es la quote del miercoles',
        'thursday' : 'Esta es la quote del jueves',
        'friday' : 'Esta es la quote del vierens',
        'saturday' : 'Esta es la quote del sábado',
        'sunday' : 'Esta es la quote del domingo',
        }

# Create your views here.

def index(request): 
    days_keys_list = list(quotes.keys())
    return render(request, 'quotes/index.html', {'days': days_keys_list})

def messages_per_day(request, day): # Imporante que el name del parametro enviado desde la url se ubique igual en la view 
    
    # Lógica implementada sin try-except
        # if day not in quotes.keys():
        #     return HttpResponseNotFound('dia no encontrado')
        # return HttpResponse(quotes[day])
    
    # Lógica implementada con try-except:
    try:
        return HttpResponse(quotes[day])
    except KeyError:
        # En teoría si se acciona este except es porqué tenemos un '404' code. Pero al aplicar render estaremos
        # mostrando un template que se carga con '200' code. Es decir en realidad no hay '404' code.
        return render(request, '404.html')
    
        # si de verdad deseamos renderizar una plantilla cuando obtengamos un '404', se tendrá que instanciar 'Http404'.
        # Pero esta opción solo esta disponible cuando el proyecto este desplegado (es decir cuando DEBUG=False)
        # return Http404() --> detecta un template con nombre '404.html' automaticamente.
    
def messages_per_day_with_number(request, day):
    days_keys_list = list(quotes.keys())

    if day < 0 or day > len(days_keys_list):
        return HttpResponseNotFound('dia no encontrado')
    # Si tenemos arg en la url, es importante detallarán su envió mediate una lista asignada a 'args':
    message_url = reverse('message_x_day', args=[days_keys_list[day-1]])
    return HttpResponseRedirect(message_url) 

def test(request):
    return render(request, 'quotes/test.html')