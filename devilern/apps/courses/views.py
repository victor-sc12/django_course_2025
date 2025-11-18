from django.shortcuts import render, get_object_or_404
from .models import Course
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def course_list(request):

    courses = Course.objects.all()
    query = request.GET.get('query')

    if query:
        courses = courses.filter(Q(title__icontains=query) | Q(owner__first_name__icontains = query))
    
    paginator = Paginator(courses, 12)
    page_obj = paginator.get_page(request.GET.get('page'))

    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    
    query_string = query_params.urlencode()

    return render(request, 'courses/courses.html', {
        'courses': page_obj,
        'query': query,
        'query_string': query_string
        })

def course_detail(request, slug):
    """
    course = {
        'title': 'Contenido del curso',
        'link':'course_lessons',
        'img': 'images/curso_2.jpg',
        'info': {
            'lessons':79,
            'hours':8,
            'instructor':'Ricardo Cuéllar',
        },
        'secciones': [
            {
                'id': 1,
                'title_section':'Introducción al curso',
                'content_section': [
                    {
                        'name': '¿Qué aprenderás en este curso?',
                        'type': 'video',
                    },
                    {
                        'name': 'Cómo usar la plataforma',
                        'type': 'file',
                    }
                ]
            },

            {
                'id':2,
                'title_section':'Fundamentos necesarios de Python',
                'content_section': [
                    {
                        'name': 'Variables y tipos de datos',
                        'type': 'video',
                    },
                    {
                        'name': 'Cómo usar la plataforma',
                        'type': 'file',
                    },
                    {
                        'name': 'Funciones básicas',
                        'type': 'video',
                    },
                ]
            },
            
            {
                'id':3,
                'title_section':'Introducción a Django',
                'content_section': [
                    {
                        'name': '¿Qué aprenderás en este curso?',
                        'type': 'file',
                    },
                    {
                        'name': 'Cómo usar la plataforma',
                        'type': 'file',
                    }
                ]
            }
        ] 
    }
    """
    # course = Course.objects.get(slug = slug)
    course = get_object_or_404(Course, slug = slug)
    modules = course.curso_modulos.prefetch_related('module_content')

    # total de clases en curso: contar cada contenido en cada modulo con un for comprimido:
    total_clases = sum(module.module_content.count() for module in modules)

    return render(request, 'courses/course_detail.html', {
        'course':course,
        'modules': modules,
        'total_clases':total_clases
        })

def course_lessons(request, slug):
    """
    lesson = {
        'title': 'Django: Crea aplicaciones web robustas con Python',
        'progress':30,
        'secciones': [
            {
                'id': 1,
                'title_section':'Introducción al curso',
                'content_section': [
                    {
                        'name': '¿Qué aprenderás en este curso?',
                        'type': 'video',
                    },
                    {
                        'name': 'Cómo usar la plataforma',
                        'type': 'file',
                    }
                ]
            },

            {
                'id':2,
                'title_section':'Fundamentos necesarios de Python',
                'content_section': [
                    {
                        'name': 'Variables y tipos de datos',
                        'type': 'video',
                    },
                    {
                        'name': 'Cómo usar la plataforma',
                        'type': 'file',
                    },
                    {
                        'name': 'Funciones básicas',
                        'type': 'video',
                    },
                ]
            },
            
            {
                'id':3,
                'title_section':'Introducción a Django',
                'content_section': [
                    {
                        'name': '¿Qué aprenderás en este curso?',
                        'type': 'file',
                    },
                    {
                        'name': 'Cómo usar la plataforma',
                        'type': 'file',
                    }
                ]
            }
        ] 
    }
    """
    course = get_object_or_404(Course, slug = slug)
    modules = course.curso_modulos.prefetch_related('module_content')
    return render(request, 'courses/course_lessons.html', {
        'course':course,
        'modules': modules,
        })