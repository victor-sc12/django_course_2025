from django.shortcuts import render
from .models import *
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    try:
        libros = Libro.objects.all()
        query_filter = request.GET.get('query_search')
        date_start = request.GET.get('start')
        date_end = request.GET.get('end')

        # capturar título o nombre de autor
        if query_filter:
            libros = libros.filter(Q(title__icontains = query_filter) | Q(autor__name__icontains = query_filter))
        
        # capturar fechas
        if date_start and date_end:
            libros = libros.filter(publication_date__range=[date_start, date_end])

        # Paginator (el paginador siempre debe ir al final de todos los filters)
        paginator = Paginator(libros, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # capturar url y sus parametros:
        query_params = request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        query_string = query_params.urlencode()

        return render(request, 'library/index.html', {
            'libros': page_obj,
            'query': query_filter,
            'query_string': query_string,
        })
    except Exception:
        return HttpResponseNotFound('Page not found')