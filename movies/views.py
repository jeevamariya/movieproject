from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import MovieForm,CommentForm
from .models import Movie,Comment,Favorite

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.added_by = request.user
            movie.save()
            return redirect('home')
    else:
        form = MovieForm()
    return render(request, 'movies/add_movie.html', {'form':form})

def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies':movies})

def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    comments = Comment.objects.filter(movie=movie)
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user,movie=movie).exists
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = CommentForm()
    return render(request, 'movies/movie_detail.html', {'movie':movie,'comments':comments,'form':form ,'is_favorite':is_favorite})

@login_required
def edit_movie(request,movie_id):
    movie = Movie.objects.get(id=movie_id)
    if movie.added_by != request.user:
        return redirect('movie_list')
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movies/edit_movie.html', {'form':form})

@login_required
def delete_movie(request,movie_id):
    movie = Movie.objects.get(id=movie_id)
    if movie.added_by != request.user:
        return redirect('movie_list')
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    return render(request, 'movies/delete_movie.html', {'movie':movie})

def search_movies(request):
    query = request.GET.get('q','')
    movies = Movie.objects.filter(title__icontains=query)
    return render(request, 'movies/search.html',{'movies':movies, 'query':query})

def category_movies(request, category_id):
    movies = Movie.objects.filter(category_id=category_id)
    return render(request, 'movies/category_movies.html', {'movies':movies})

@login_required
def toggle_favorite(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    favorite = Favorite.objects.filter(user=request.user,movie=movie).first()
    if favorite:
        favorite.delete()
    else:
        Favorite.objects.create(user=request.user,movie=movie)
    return redirect('movie_detail',movie_id=movie.id)

@login_required
def favorite_movies(request):
    favorites = Favorite.objects.filter(user=request.user)
    movies = [favorite.movie for favorite in favorites]
    return render(request, 'movies/favorite_movies.html',{'movies':movies})