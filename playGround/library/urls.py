from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recomendar/<int:book_id>', views.add_review ,name="recommend_book"),
    path('add-libro/', views.add_libro, name='add_libro'),
     
    # Se debe emplear el método 'as.view()' si la vista es cbv:
    path('greet/', views.Greet.as_view(), name='greet_cbv'),
    path('welcomo/', views.WelcomoGreet.as_view(), name='wlc_greet'),
    path('libros/', views.LibroListView.as_view(), name='libro_list'),
    path('libro/<int:pk>/detail/', views.LibroDetailView.as_view(), name='libro_detail'),
    path('review/<int:pk>/create/', views.ReviewCreateView.as_view(), name='add_review'),
    path('libro/<int:pk>/update/', views.LibroUpdateView.as_view(), name='libro_update'),
    path('review/<int:pk>/update/', views.ReviewUpdateView.as_view(), name='update_review'),
    path('review/<int:pk>/delete/', views.ReviewDeleteView.as_view(), name='delete_review'),
    path('visitas/', views.visit_counter, name='session_visitas'),
]