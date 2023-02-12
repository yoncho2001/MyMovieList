from django.shortcuts import render, redirect
from .forms import MovieForm
from .models import Movie

def movie_list(request):
    movies = Movie.objects.all()
    if request.method == "POST":
        if request.POST.get("title"):
            title = request.POST["title"]
            year = request.POST["year"]
            rating = request.POST["rating"]
            movie = Movie(title=title, year=year, rating=rating)
            movie.save()
            return redirect("movie_list")
    return render(request, "movie_list.html", {"movies": movies})

def delete_movie(request, id):
    movie = Movie.objects.get(id=id)
    movie.delete()
    return redirect("movie_list")

def movie_detail(request, pk):
    movie = Movie.objects.get(pk=pk)
    return render(request, 'movie_detail.html', {'movie': movie})

def movie_add(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieForm()
    return render(request, 'movie_form.html', {'form': form})

def movie_edit(request, pk):
    movie = Movie.objects.get(pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            movie = form.save()
            return redirect('movie_detail', pk=movie.pk)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'movie_form.html', {'form': form})
