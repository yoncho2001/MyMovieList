from django.test import TestCase
from django.urls import reverse
from .models import MovieList, Movie
from .forms import MovieForm


class MovieListTestCase(TestCase):
    def setUp(self):
        self.movie_list = MovieList.objects.create(name='Action Movies')
        self.movie1 = Movie.objects.create(
            title='The Matrix', year=1999, rating=8.7, movie_list=self.movie_list)
        self.movie2 = Movie.objects.create(
            title='Terminator 2', year=1991, rating=8.5, movie_list=self.movie_list)

    def test_movie_list_view(self):
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movie_list.html')
        self.assertContains(response, 'Action Movies')

    def test_movie_list_detail_view(self):
        response = self.client.get(
            reverse('movie_list_detail', args=[self.movie_list.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movie_list_detail.html')
        self.assertContains(response, 'The Matrix')
        self.assertContains(response, 'Terminator 2')

    def test_create_movie_list_view(self):
        response = self.client.post(reverse('create_movie_list'), {
                                    'name': 'Comedy Movies'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MovieList.objects.count(), 2)

    def test_create_movie_view(self):
        response = self.client.post(reverse('create_movie', args=[self.movie_list.pk]), {
                                    'title': 'The Terminator', 'year': 1984, 'rating': 8.0})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Movie.objects.count(), 3)

    def test_delete_movie(self):
        response = self.client.post(
            reverse('delete_movie', args=[self.movie_list.pk, self.movie1.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Movie.objects.count(), 1)

    def test_delete_movie_list(self):
        response = self.client.post(
            reverse('delete_movie_list', args=[self.movie_list.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(MovieList.objects.count(), 0)


class EditMovieTest(TestCase):
    def setUp(self):
        self.movie_list = MovieList.objects.create(name="Test Movie List")
        self.movie = Movie.objects.create(
            title="Test Movie",
            year=2020,
            rating=4.5,
            movie_list=self.movie_list
        )

    def test_edit_movie(self):
        response = self.client.get(
            reverse('edit_movie', args=[self.movie_list.pk, self.movie.pk]))
        self.assertEqual(response.status_code, 200)

        self.assertIsInstance(response.context['form'], MovieForm)

        response = self.client.post(reverse('edit_movie', args=[self.movie_list.pk, self.movie.pk]), data={
            'title': "Test Movie 2",
            'year': 2021,
            'rating': 4.0
        })
        self.assertEqual(response.status_code, 302)

        movie = Movie.objects.get(pk=self.movie.pk)
        self.assertEqual(movie.title, "Test Movie 2")
        self.assertEqual(movie.year, 2021)
        self.assertEqual(movie.rating, 4.0)
