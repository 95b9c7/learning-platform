from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile


class Command(BaseCommand):
    help = 'Create a demo user for testing'

    def handle(self, *args, **options):
        # Create demo user if it doesn't exist
        username = 'demo'
        email = 'demo@safeoperatorpro.com'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Demo user "{username}" already exists')
            )
            return
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password='demo123',
            first_name='Demo',
            last_name='User'
        )
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            bio='Demo user for SafeOperator Pro testing',
            user_type='student'
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Demo user "{username}" created successfully')
        )
        self.stdout.write(f'Email: {email}')
        self.stdout.write('Password: demo123')
