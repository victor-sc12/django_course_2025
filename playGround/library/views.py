from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponse
from django.core.paginator import Paginator
from .forms import ReviewSimpleForm, ReviewForm, LibroForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

User = get_user_model()

# Creación de vistas CBV:
class Greet(View):
    def get(self, request):
        return HttpResponse('Hello from CBV')
    
class WelcomoGreet(TemplateView):
    template_name = 'library/welcomo_greet.html'

    # método genérico para implementar 'context' data en una 'TemplateView' class
    def get_context_data(self, **kwargs):
        
        # obtener toda la configuración inicial del 'get_context_data' de la clase padre:
        context = super().get_context_data(**kwargs)
        
        # adicionar data propia al context original:
        context['total_books'] = Libro.objects.count()
        
        return context

class LibroListView(ListView):
    # Especificar el modelo para que 'ListView' gestione intarnamente el queryset 
    model = Libro

    # En teoría la 'ListView' ubica el template. Pero es buena práctica especificarlo:
    template_name = 'library/libro_list.html'
    
    # El contexto por defecto se nombra como 'object_list', pero se puede cambiar: 
    context_object_name = 'libros'

    # 'ListView' viene con un paginador incluido:
    paginate_by = 5

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'library/libro_detail.html'
    context_object_name = 'book'

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'library/add_review.html'

    def form_valid(self, form):
        
        # acceder al arg 'pk' de url mediante los kwargs:
        libro_id = self.kwargs['pk']
        libro = Libro.objects.get(id=libro_id)
        
        # aca el form obj ya es identificado y gestionado automaticamente por django y la cbv,
        # así que podemos acceder a este sin problema:
        form.instance.libro = libro
        form.instance.usuario = User.objects.get(username__icontains = 'bycadmin')
        
        messages.success(self.request, "Gracias por tu review.")
        
        # Retorno de 'form_valid' heredado ya con el nuevo formulario: 
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('libro_detail', kwargs={"pk": self.kwargs['pk']})

class LibroUpdateView(UpdateView):
    model = Libro
    # form_class = LibroForm
    fields = ['title', 'isbn', 'pages', 'publication_date',]
    template_name = 'library/libro_update.html'

    def form_valid(self, form):
        messages.success(self.request, "El libro ha sido actualizado con éxito")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ha ocurrido un error en la actualuzación.", "danger")
        return super().form_invalid(form)

    def get_success_url(self):
        libro_pk = self.kwargs['pk']
        return reverse_lazy('libro_detail', kwargs={"pk":libro_pk})
    
    # Acá se esta sobreescribiendo el método 'get_context_data' para exteder el diccionario de contexto: 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['libro'] = Libro.objects.get(id = self.kwargs['pk'])
        return context

class ReviewUpdateView(UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'library/add_review.html' # se reutiliza el form template de añadir review porque se piden los mismo fields

    def form_valid(self, form):
        form.instance 
        messages.success(self.request, "La reseña se actualizó correctamente.")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, "No se puedo actualizar la review", "danger")
        return super().form_invalid(form)

    def get_queryset(self):

        # Acá limitamos a que el query de reviews se limite a la del uuario 'bycadmin'.
        # Esto es un pseudo control para que los usuarios puedan editar únicamente sus reviews
        return Review.objects.filter(usuario__username__icontains = "bycadmin")
    
    def get_success_url(self):
        review = Review.objects.get(id = self.kwargs['pk'])
        libro_id = review.libro.id
        return reverse_lazy('libro_detail', kwargs={"pk":libro_id})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        review = Review.objects.get(id = self.kwargs['pk'])
        libro = Libro.objects.get(id = review.libro.id)
        context['libro'] = libro
        return context

class ReviewDeleteView(DeleteView):
    model = Review
    template_name = 'library/review_confirm_delete.html'
    success_url = reverse_lazy('libro_list')
    
    def get_queryset(self):
        # se tendrá control únicamente de los review querys que corresponden al usuario especificado,
        # es una pseudo validación de usuario registrada
        return Review.objects.filter(usuario__username__icontains = "bycadmin")

    def delete(self, request, *args, **kwargs):

        # sobreescribir este método para agregar el mensaje de éxito en eliminación:
        messages.success(self.request, "Review eliminada correctamente")

        return super().delete(request, *args, **kwargs)

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
    form = ReviewForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # Se guarda la info momentanea del form pero todavía no se envía a la db (gracias a commit = 'False'),
            # esto permite que aún poblemos los otros atributos que están pendientes, como libro y usuario. 
            review = form.save(commit=False)  
            review.libro = libro
            review.usuario = request.user
            review.save()

            # Gestión del nuevo campo del form (se ubica después de guardar la info en la db, porque obvio
            # no se puede guardar la info de este field en el modelo):
            would_recommend = form.cleaned_data.get('would_recommend')

            if would_recommend:
                messages.success(request, 'Review y recomendación definidos correctamente.')
            else:   
                messages.success(request, "Review realizada correctamente.")
            return redirect("recommend_book", book_id = book_id) 
        
        else:
            messages.error(request, 'corrige los errores del form', "danger")
    
    return render(request, 'library/add_review.html', {
        'form':form, 
        'libro':libro 
    })

def add_libro(request):

    if request.method == 'POST':

        form = LibroForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, 'Libro ingresado correctamente.')   
            return redirect('add_libro')

        else:
            messages.success(request, "Soluciona los errores.", "danger")

    else:
        form = LibroForm()

    return render(request, 'library/add_libro.html', {'form':form})