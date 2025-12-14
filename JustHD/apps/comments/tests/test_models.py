from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.comments.models import Comment
from apps.movies.models import Movie, Genre

User = get_user_model()

class CommentModelTest(TestCase):
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

    def test_comment_creation(self):
        comment = Comment.objects.create(
            user=self.user,
            movie=self.movie,
            text='Great movie!'
        )
        
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.movie, self.movie)
        self.assertEqual(comment.text, 'Great movie!')
        self.assertTrue(comment.is_active)
        self.assertIsNone(comment.parent)

    def test_comment_with_parent(self):
        parent_comment = Comment.objects.create(
            user=self.user,
            movie=self.movie,
            text='Parent comment'
        )
        
        reply_comment = Comment.objects.create(
            user=self.user,
            movie=self.movie,
            text='Reply comment',
            parent=parent_comment
        )
        
        self.assertEqual(reply_comment.parent, parent_comment)
        self.assertTrue(parent_comment.replies.filter(id=reply_comment.id).exists())

    def test_comment_soft_delete(self):
        comment = Comment.objects.create(
            user=self.user,
            movie=self.movie,
            text='Test comment'
        )
        
        comment.is_active = False
        comment.save()
        
        self.assertFalse(comment.is_active)
        self.assertNotIn(comment, Comment.objects.filter(is_active=True))

    def test_has_replies_property(self):
        parent_comment = Comment.objects.create(
            user=self.user,
            movie=self.movie,
            text='Parent comment'
        )

        self.assertFalse(parent_comment.has_replies)
        
        Comment.objects.create(
            user=self.user,
            movie=self.movie,
            text='Reply comment',
            parent=parent_comment
        )
        
        parent_comment.refresh_from_db()
        self.assertTrue(parent_comment.has_replies)