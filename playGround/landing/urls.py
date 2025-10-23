from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('tools/<str:tool>/', views.tool_view, name='tools'),
]