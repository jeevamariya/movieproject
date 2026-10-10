from django.urls import path
from . import views

urlpatterns = [
    path('movies/add/', views.add_movie, name='add_movie'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:movie_id>/edit/', views.edit_movie, name='edit_movie'),
    path('movies/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
    path('search/', views.search_movies, name='search_movies'),
    path('category/<int:category_id>/', views.category_movies, name='category_movies'),
    path('movies/<int:movie_id>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorite_movies, name='favorite_movies'),
]