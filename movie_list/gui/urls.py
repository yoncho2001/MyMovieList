from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('<int:pk>/', views.movie_detail, name='movie_detail'),
    path('add/', views.movie_add, name='movie_add'),
    path('<int:pk>/edit/', views.movie_edit, name='movie_edit'),
    path("<int:id>/delete/", views.delete_movie, name="delete_movie"),
]