from django.shortcuts import render

# Create your views here.
def course_list(request):
    # query simulator:
    courses = [
        {
            'id': 1,
            'img': 'images/curso_1.jpg',
            'level': 'Beginner',
            'rating': 5.0,
            'title': 'Three-month Course to Learn the Basics of Python and Start Coding.',
            'author_img': 'https://randomuser.me/api/portraits/men/77.jpg',
            'author_name': 'Alison Walsh',
        },
        {
            'id': 2,
            'img': 'images/curso_2.jpg',
            'level': 'Beginner',
            'rating': 5.0,
            'title': 'Three-month Course to Learn the Basics of Python and Start Coding.',
            'author_img': 'https://randomuser.me/api/portraits/men/1.jpg',
            'author_name': 'Alison Walsh',
        },
        {
            'id': 3,
            'img': 'images/curso_3.jpg',
            'level': 'Beginner',
            'rating': 5.0,
            'title': 'Three-month Course to Learn the Basics of Python and Start Coding.',
            'author_img': 'https://randomuser.me/api/portraits/women/18.jpg',
            'author_name': 'Alison Walsh',
        },
        {
            'id': 4,
            'img': 'images/curso_4.jpg',
            'level': 'Beginner',
            'rating': 5.0,
            'title': 'Three-month Course to Learn the Basics of Python and Start Coding.',
            'author_img': 'https://randomuser.me/api/portraits/women/29.jpg',
            'author_name': 'Alison Walsh',
        },
        {
            'id': 5,
            'img': 'images/curso_5.jpg',
            'level': 'Beginner',
            'rating': 5.0,
            'title': 'Three-month Course to Learn the Basics of Python and Start Coding.',
            'author_img': 'https://randomuser.me/api/portraits/women/45.jpg',
            'author_name': 'Alison Walsh',
        },
    ]
    return render(request, 'courses/courses.html', {'courses':courses})

def course_detail(request):
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
    return render(request, 'courses/course_detail.html', {'course':course})

def course_lessons(request):
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
    return render(request, 'courses/course_lessons.html', {'lesson': lesson})