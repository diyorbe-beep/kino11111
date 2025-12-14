from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.ratings.models import Rating
from apps.movies.models import Movie, Genre

User = get_user_model()

class RatingModelTest(TestCase):
    def setUp(self):
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

    def test_rating_creation(self):
        rating = Rating.objects.create(
            user=self.user,
            movie=self.movie,
            score=8,
            comment='Great movie!'
        )
        
        self.assertEqual(rating.user, self.user)
        self.assertEqual(rating.movie, self.movie)
        self.assertEqual(rating.score, 8)
        self.assertEqual(rating.comment, 'Great movie!')

    def test_rating_score_validation(self):
        rating_min = Rating(
            user=User.objects.create_user(
                username='user1', 
                email='user1@example.com',
                password='testpass123'
            ),
            movie=self.movie,
            score=1
        )
        rating_min.save()
        self.assertEqual(rating_min.score, 1)

        rating_max = Rating(
            user=User.objects.create_user(
                username='user2',
                email='user2@example.com', 
                password='testpass123'
            ),
            movie=self.movie,
            score=10
        )
        rating_max.save()
        self.assertEqual(rating_max.score, 10)
        
    def test_rating_unique_constraint(self):
        Rating.objects.create(
            user=self.user,
            movie=self.movie,
            score=8
        )

        with self.assertRaises(Exception):
            Rating.objects.create(
                user=self.user,
                movie=self.movie,
                score=9
            )

    def test_rating_string_representation(self):
        rating = Rating.objects.create(
            user=self.user,
            movie=self.movie,
            score=8
        )
        
        expected_str = f"{self.user.username} - {self.movie.title}: 8/10"
        self.assertEqual(str(rating), expected_str)