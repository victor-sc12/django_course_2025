from django.shortcuts import render
from .models import *
from django.http import HttpResponseNotFound

# Create your views here.
def index(request):
    try:
        libros = Libro.objects.all()
        autor_id = request.GET.get('autor')
        genero_id = request.GET.get('genero')

        if autor_id and genero_id:
            libros = libros.filter(autor__id = autor_id)
            autor = Autor.objects.get(id = autor_id)

        if genero_id:
            libros = libros.filter(generos__id = genero_id)
            genero = Genero.objects.get(id=genero_id)

        return render(request, 'library/index.html', {
            'libros': libros,
            'autor': autor,
            'genero': genero,
        })
    except Exception:
        return HttpResponseNotFound('Page not found')