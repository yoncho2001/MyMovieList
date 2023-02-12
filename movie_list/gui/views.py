from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import MovieListForm, MovieForm
from .models import MovieList, Movie


def movie_list(request):
    movie_lists = MovieList.objects.all()
    return render(request, 'movie_list.html', {'movie_lists': movie_lists})


def movie_list_detail(request, pk):
    movie_list = MovieList.objects.get(pk=pk)
    movies = movie_list.movie_set.all()
    return render(request, 'movie_list_detail.html', {'movie_list': movie_list, 'movies': movies})


def create_movie_list(request):
    if request.method == 'POST':
        form = MovieListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieListForm()
    return render(request, 'create_movie_list.html', {'form': form})


def create_movie(request, pk):
    movie_list = MovieList.objects.get(pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.movie_list = movie_list
            movie.save()
            return redirect('movie_list_detail', pk=pk)
    else:
        form = MovieForm()
    return render(request, 'create_movie.html', {'form': form})


def delete_movie(request, pk, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    movie.delete()
    return redirect('movie_list_detail', pk=pk)


def delete_movie_list(request, pk):
    movie_list = MovieList.objects.get(pk=pk)
    if request.method == 'POST':
        movie_list.delete()
        return redirect('movie_list')
    return render(request, 'delete_movie_list.html', {'movie_list': movie_list})


def edit_movie(request, pk, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_list_detail', pk=pk)
    else:
        form = MovieForm(instance=movie)

    return render(request, 'edit_movie.html', {'form': form})
