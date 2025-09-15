from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a gen_ai_serviceuser for AI-generated content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='gen_ai_serviceuser',
            help='Username for the GenAI service user (default: gen_ai_serviceuser)'
        )
        parser.add_argument(
            '--email',
            type=str,
            default='genai@retrospectives.local',
            help='Email for the GenAI service user (default: genai@retrospectives.local)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force creation even if user already exists'
        )

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        force = options['force']

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            if not force:
                self.stdout.write(
                    self.style.WARNING(
                        f'User "{username}" already exists. Use --force to recreate.'
                    )
                )
                return
            else:
                # Delete existing user
                User.objects.filter(username=username).delete()
                self.stdout.write(
                    self.style.WARNING(f'Deleted existing user "{username}"')
                )

        # Create the GenAI service user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=None,  # No password needed for service user
                first_name='GenAI',
                last_name='Service',
                is_active=True,
                is_staff=False,
                is_superuser=False
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created GenAI service user: "{username}" (ID: {user.id})'
                )
            )
            
            # Display user details
            self.stdout.write(f'  Username: {user.username}')
            self.stdout.write(f'  Email: {user.email}')
            self.stdout.write(f'  Full Name: {user.first_name} {user.last_name}')
            self.stdout.write(f'  Active: {user.is_active}')
            self.stdout.write(f'  Staff: {user.is_staff}')
            self.stdout.write(f'  Superuser: {user.is_superuser}')
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating user: {str(e)}')
            )
            raise
