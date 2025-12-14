from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.ratings.models import Rating
from apps.movies.models import Movie, Genre
from django.urls import reverse

User = get_user_model()

class RatingViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        
        self.genre = Genre.objects.create(name='Action', slug='action')
        self.movie = Movie.objects.create(
            title='Test Movie',
            slug='test-movie',
            description='Test description',
            release_year=2023,
            duration=120
        )
        self.movie.genres.add(self.genre)
        
        self.rating = Rating.objects.create(
            user=self.user,
            movie=self.movie,
            score=8,
            comment='Good movie'
        )
        
        self.rating_list_url = reverse('ratings:rating-list')
        self.rating_create_url = reverse('ratings:rating-create')
        self.rating_detail_url = reverse('ratings:rating-detail', kwargs={'pk': self.rating.pk})
        self.movie_ratings_url = reverse('ratings:movie-ratings', kwargs={'movie_slug': self.movie.slug})

    def _get_response_data(self, response):
        if 'data' in response.data:
            return response.data['data']
        return response.data

    def test_rating_list_unauthenticated(self):
        response = self.client.get(self.rating_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = self._get_response_data(response)
        self.assertIn('results', response_data)

    def test_rating_create_authenticated(self):
        self.client.force_authenticate(user=self.other_user)
        
        data = {
            'movie': self.movie.id,
            'score': 9,
            'comment': 'Excellent movie!'
        }
        
        response = self.client.post(self.rating_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response_data = self._get_response_data(response)
        self.assertEqual(response_data['score'], 9)

    def test_rating_create_duplicate(self):
        self.client.force_authenticate(user=self.user)
        
        data = {
            'movie': self.movie.id,
            'score': 9
        }
        
        response = self.client.post(self.rating_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rating_create_invalid_score(self):
        self.client.force_authenticate(user=self.other_user)
        
        data = {
            'movie': self.movie.id,
            'score': 11
        }
        
        response = self.client.post(self.rating_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rating_update_owner(self):
        self.client.force_authenticate(user=self.user)
        
        data = {'score': 10, 'comment': 'Updated review'}
        response = self.client.patch(self.rating_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['score'], 10)

    def test_rating_update_non_owner(self):
        self.client.force_authenticate(user=self.other_user)
        
        data = {'score': 5}
        response = self.client.patch(self.rating_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_movie_ratings(self):
        response = self.client.get(self.movie_ratings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)