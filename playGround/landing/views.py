from django.shortcuts import render
from django.http import HttpResponse
from datetime import date

# Create your views here.

def index(request):
    # Empleando función 'render' en lugar de 'HttpResponse()'
    today = date.today()
    name = 'Ricardo'
    lista = [
        {'id':'python', 'name':'Python'}, 
        {'id':'html', 'name':'HTML'}, 
        {'id':'ruby', 'name':'Ruby'}, 
        {'id':'larabel', 'name':'Larabel'}
        ]
    return render(request, 'landing/index.html', context={'name':name, 'today':today, 'lista':lista})

def tool_view(request, tool):
    return HttpResponse(f'Tecnología: {tool}')