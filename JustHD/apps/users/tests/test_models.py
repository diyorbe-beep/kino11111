from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.users.models import UserProfile

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertFalse(self.user.is_premium)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)

    def test_user_profile_auto_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
        self.assertEqual(self.user.profile.language, 'en')
        self.assertEqual(self.user.profile.theme, 'light')

    def test_user_full_name(self):
        self.assertEqual(self.user.full_name, 'Test User')

    def test_user_string_representation(self):
        self.assertEqual(str(self.user), 'testuser')

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='profiletest',
            email='profile@example.com',
            password='testpass123'
        )
        self.profile = self.user.profile

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.language, 'en')
        self.assertEqual(self.profile.theme, 'light')
        self.assertTrue(self.profile.notifications_enabled)
        self.assertTrue(self.profile.email_notifications)

    def test_profile_string_representation(self):
        self.assertEqual(str(self.profile), "profiletest's Profile")