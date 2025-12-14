from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.movies.models import Movie, Genre
from django.urls import reverse

User = get_user_model()

class MovieViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.regular_user = User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='testpass123'
        )
        
        self.premium_user = User.objects.create_user(
            username='premiumuser',
            email='premium@example.com',
            password='testpass123',
            is_premium=True
        )
        
        self.genre = Genre.objects.create(name='Action', slug='action')
        
        self.regular_movie = Movie.objects.create(
            title='Test Movie',
            slug='test-movie',
            description='Test description',
            release_year=2023,
            duration=120,
            is_premium=False,
            is_active=True
        )
        self.regular_movie.genres.add(self.genre)

        self.premium_movie = Movie.objects.create(
            title='Premium Movie',
            slug='premium-movie', 
            description='Premium description',
            release_year=2023,
            duration=120,
            is_premium=True,
            is_active=True
        )
        self.premium_movie.genres.add(self.genre)

    def _get_response_data(self, response):
        if 'data' in response.data:
            return response.data['data']
        return response.data

    def test_movie_list_unauthenticated(self):
        url = reverse('movies:movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = self._get_response_data(response)
        self.assertIn('results', response_data)

        movies = response_data['results']
        movie_titles = [movie['title'] for movie in movies]
        self.assertIn('Test Movie', movie_titles)
        self.assertNotIn('Premium Movie', movie_titles)

    def test_movie_list_authenticated_regular(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('movies:movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = self._get_response_data(response)
        movies = response_data['results']
        movie_titles = [movie['title'] for movie in movies]
        
        self.assertIn('Test Movie', movie_titles)
        self.assertNotIn('Premium Movie', movie_titles)

    def test_movie_list_authenticated_premium(self):
        self.client.force_authenticate(user=self.premium_user)
        url = reverse('movies:movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = self._get_response_data(response)
        movies = response_data['results']
        
        self.assertEqual(len(movies), 2)
        movie_titles = [movie['title'] for movie in movies]
        self.assertIn('Test Movie', movie_titles)
        self.assertIn('Premium Movie', movie_titles)

    def test_movie_detail(self):
        url = reverse('movies:movie-detail', kwargs={'slug': self.regular_movie.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = self._get_response_data(response)
        self.assertEqual(response_data['title'], 'Test Movie')

    def test_movie_detail_increments_views(self):
        initial_views = self.regular_movie.views_count
        url = reverse('movies:movie-detail', kwargs={'slug': self.regular_movie.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.regular_movie.refresh_from_db()
        self.assertEqual(self.regular_movie.views_count, initial_views + 1)

    def test_premium_movie_access_regular_user(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('movies:movie-watch', kwargs={'slug': self.premium_movie.slug})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_premium_movie_access_premium_user(self):
        self.client.force_authenticate(user=self.premium_user)
        url = reverse('movies:movie-watch', kwargs={'slug': self.premium_movie.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = self._get_response_data(response)
        self.assertEqual(response_data['title'], 'Premium Movie')

    def test_search_movies(self):
        url = reverse('movies:movie-search')
        response = self.client.get(url, {'q': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = self._get_response_data(response)
        self.assertIn('results', response_data)
        self.assertIn('query', response_data)

    def test_genre_list(self):
        url = reverse('movies:genre-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = self._get_response_data(response)
        self.assertIsInstance(response_data, list)

    def test_movie_watch_regular_movie(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('movies:movie-watch', kwargs={'slug': self.regular_movie.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movie_watch_premium_movie_premium_user(self):
        self.client.force_authenticate(user=self.premium_user)
        url = reverse('movies:movie-watch', kwargs={'slug': self.premium_movie.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)