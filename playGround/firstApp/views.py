from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # return HttpResponse(htmlMenu + "<p>Hola Mundito, esto es una portada.</p>")
    return render(request, 'firstApp/home.html')

def about(request):
    # return HttpResponse(htmlMenu + '<p>Hola de nuevo worldsito, es una ventana de about</p>')
    return render(request, 'firstApp/about.html')

def contacto(request):
    # return HttpResponse(htmlMenu + '<p>Hola de nuevo worldsito, es una ventana de contacto</p>')
    return render(request, 'firstApp/contacto.html')

def portafolio(request):
    # return HttpResponse(htmlMenu + '<p>Hola de nuevo worldsito, es una ventana de portafolio</p>')
    return render(request, 'firstApp/portafolio.html')