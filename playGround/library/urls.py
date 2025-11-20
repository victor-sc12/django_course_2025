from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recomendar/<int:book_id>', views.add_review ,name="recommend_book")
]