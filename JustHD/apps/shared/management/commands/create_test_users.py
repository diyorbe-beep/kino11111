from django.core.management.base import BaseCommand
from apps.users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('👥 Creating test users...')
        
        test_users = [
            {
                'username': 'testuser',
                'email': 'test@justhd.com',
                'password': 'testpass123',
                'first_name': 'Test',
                'last_name': 'User',
            },
            {
                'username': 'premiumuser',
                'email': 'premium@justhd.com',
                'password': 'premium123',
                'first_name': 'Premium',
                'last_name': 'User',
            },
        ]
        
        for user_data in test_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f'✅ Created user: {user.username}')
            else:
                self.stdout.write(f'ℹ️  User already exists: {user.username}')
        
        self.stdout.write(self.style.SUCCESS('✅ Test users created successfully!'))