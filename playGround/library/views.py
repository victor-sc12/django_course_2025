from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator
from .forms import ReviewSimpleForm
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()

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

def add_review(request, book_id):
    libro = get_object_or_404(Libro, id=book_id)
    form = ReviewSimpleForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            rating = form.cleaned_data['rating']
            text = form.cleaned_data['text']
            user = request.user if request.user.is_authenticated else User.objects.first() 

            Review.objects.create(rating=rating, text=text, usuario=user, libro=libro)

            messages.success(request, 'Grcias por la reseña')
            return redirect('recommend_book', book_id=book_id)
        
        else:
            messages.error(request, 'corrige los errores del form')
    
    return render(request, 'library/add_review.html', {
        'form':form, 
        'libro':libro 
    })