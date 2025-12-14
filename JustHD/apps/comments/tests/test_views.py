from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.comments.models import Comment
from apps.movies.models import Movie, Genre
from django.urls import reverse

User = get_user_model()

class CommentViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
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
        
        self.comment = Comment.objects.create(
            user=self.user,
            movie=self.movie,
            text='Test comment'
        )
        
        self.comment_list_url = reverse('comments:comment-list')
        self.comment_create_url = reverse('comments:comment-create')
        self.comment_detail_url = reverse('comments:comment-detail', kwargs={'pk': self.comment.pk})
        self.comment_reply_url = reverse('comments:comment-reply', kwargs={'pk': self.comment.pk})
        self.movie_comments_url = reverse('comments:movie-comments', kwargs={'movie_slug': self.movie.slug})

    def _get_response_data(self, response):
        if 'data' in response.data:
            return response.data['data']
        return response.data

    def test_comment_list_unauthenticated(self):
        response = self.client.get(self.comment_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = self._get_response_data(response)
        self.assertIn('results', response_data)

    def test_comment_create_authenticated(self):
        self.client.force_authenticate(user=self.user)
        
        data = {
            'movie': self.movie.id,
            'text': 'New test comment'
        }
        
        response = self.client.post(self.comment_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response_data = self._get_response_data(response)
        self.assertEqual(response_data['text'], 'New test comment')

    def test_comment_create_unauthenticated(self):
        data = {
            'movie': self.movie.id,
            'text': 'New test comment'
        }
        
        response = self.client.post(self.comment_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_detail(self):
        response = self.client.get(self.comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = self._get_response_data(response)
        self.assertEqual(response_data['text'], 'Test comment')

    def test_comment_update_owner(self):
        self.client.force_authenticate(user=self.user)
        
        data = {'text': 'Updated comment text'}
        response = self.client.patch(self.comment_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = self._get_response_data(response)
        self.assertEqual(response_data['text'], 'Updated comment text')

    def test_comment_reply(self):
        self.client.force_authenticate(user=self.user)
        
        data = {
            'movie': self.movie.id,
            'text': 'Reply to comment'
        }
        
        response = self.client.post(self.comment_reply_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        response_data = self._get_response_data(response)
        self.assertEqual(response_data['text'], 'Reply to comment')

    def test_movie_comments(self):
        response = self.client.get(self.movie_comments_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        response_data = self._get_response_data(response)
        self.assertIsInstance(response_data, list)

    def test_comment_delete(self):
        self.client.force_authenticate(user=self.user)
        
        response = self.client.delete(self.comment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.comment.refresh_from_db()
        self.assertFalse(self.comment.is_active)