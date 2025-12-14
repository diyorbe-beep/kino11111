from django.test import TestCase
from apps.movies.models import Genre, Movie, Video
from apps.users.models import User

class GenreModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(
            name='Action',
            description='Action movies'
        )

    def test_genre_creation(self):
        self.assertEqual(self.genre.name, 'Action')
        self.assertEqual(self.genre.slug, 'action')
        self.assertEqual(str(self.genre), 'Action')

class MovieModelTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Action')
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test description',
            release_year=2023,
            duration=120,
            is_premium=False
        )
        self.movie.genres.add(self.genre)

    def test_movie_creation(self):
        self.assertEqual(self.movie.title, 'Test Movie')
        self.assertEqual(self.movie.slug, 'test-movie')
        self.assertEqual(self.movie.release_year, 2023)
        self.assertFalse(self.movie.is_premium)
        self.assertTrue(self.movie.is_active)

class VideoModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title='Test Movie',
            description='Test description',
            release_year=2023,
            duration=120
        )
        self.video = Video.objects.create(
            movie=self.movie,
            quality='HD',
            size=1024000,
            duration=7200
        )

    def test_video_creation(self):
        self.assertEqual(self.video.movie, self.movie)
        self.assertEqual(self.video.quality, 'HD')
        self.assertEqual(self.video.size, 1024000)
        self.assertEqual(str(self.video), 'Test Movie - HD')