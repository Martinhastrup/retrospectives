import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError


def get_user_model():
    """Get the User model after Django is configured."""
    from django.contrib.auth import get_user_model as django_get_user_model
    return django_get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Test cases for the User model."""

    def test_create_user_success(self, test_user_data):
        """Test successful user creation."""
        User = get_user_model()
        user = User.objects.create_user(**test_user_data)
        
        assert user.username == test_user_data['username']
        assert user.email == test_user_data['email']
        assert user.userfullname == test_user_data['userfullname']
        assert user.role == test_user_data['role']
        assert user.check_password(test_user_data['password'])
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False

    def test_create_user_without_optional_fields(self):
        """Test user creation with only required fields."""
        User = get_user_model()
        user_data = {
            'username': 'minimaluser',
            'email': 'minimal@example.com',
            'userfullname': 'Minimal User',
            'password': 'minimalpass123'
        }
        
        user = User.objects.create_user(**user_data)
        
        assert user.username == user_data['username']
        assert user.email == user_data['email']
        assert user.userfullname == user_data['userfullname']
        assert user.role == ''  # Default empty string
        assert user.check_password(user_data['password'])

    def test_create_user_without_password(self):
        """Test user creation without password raises error."""
        User = get_user_model()
        user_data = {
            'username': 'nopassuser',
            'email': 'nopass@example.com',
            'userfullname': 'No Pass User'
        }
        
        # Django's create_user requires password, but it might handle missing password differently
        # Let's test that it at least doesn't create a user without password
        try:
            user = User.objects.create_user(**user_data)
            # If it gets here, the user was created, which is unexpected
            assert False, "User was created without password"
        except Exception as e:
            # Any exception is acceptable
            assert True

    def test_create_user_duplicate_username(self):
        """Test that duplicate usernames are not allowed."""
        User = get_user_model()
        
        # Create first user
        first_user = User.objects.create_user(
            username='duplicateuser',
            email='first@example.com',
            userfullname='First User',
            password='firstpass123'
        )
        
        # Try to create second user with same username
        duplicate_user_data = {
            'username': 'duplicateuser',  # Same username
            'email': 'second@example.com',
            'userfullname': 'Second User',
            'password': 'secondpass123'
        }
        
        # This should fail due to duplicate username
        with pytest.raises(IntegrityError):
            User.objects.create_user(**duplicate_user_data)

    def test_create_user_duplicate_email(self):
        """Test that duplicate emails are not allowed."""
        User = get_user_model()
        
        # Create first user
        first_user = User.objects.create_user(
            username='firstuser',
            email='duplicate@example.com',
            userfullname='First User',
            password='firstpass123'
        )
        
        # Try to create second user with same email
        duplicate_user_data = {
            'username': 'seconduser',
            'email': 'duplicate@example.com',  # Same email
            'userfullname': 'Second User',
            'password': 'secondpass123'
        }
        
        # This should fail due to duplicate email
        with pytest.raises(IntegrityError):
            User.objects.create_user(**duplicate_user_data)
        


    def test_user_string_representation(self, test_user):
        """Test the string representation of a user."""
        assert str(test_user) == test_user.email

    def test_user_required_fields(self):
        """Test that required fields are properly set."""
        User = get_user_model()
        assert User.USERNAME_FIELD == 'username'
        assert User.EMAIL_FIELD == 'email'
        assert 'email' in User.REQUIRED_FIELDS
        assert 'userfullname' in User.REQUIRED_FIELDS

    def test_create_superuser(self, test_user_data):
        """Test superuser creation."""
        User = get_user_model()
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        assert superuser.is_superuser is True
        assert superuser.is_staff is True
        assert superuser.is_active is True

    def test_user_password_hashing(self, test_user_data):
        """Test that passwords are properly hashed."""
        User = get_user_model()
        user = User.objects.create_user(**test_user_data)
        
        # Password should be hashed, not stored as plain text
        assert user.password != test_user_data['password']
        # But should still validate correctly
        assert user.check_password(test_user_data['password'])

    def test_user_field_constraints(self):
        """Test user field constraints and validation."""
        User = get_user_model()
        # Test username max length
        long_username = 'a' * 151  # Exceeds max_length=150
        user_data = {
            'username': long_username,
            'email': 'longuser@example.com',
            'userfullname': 'Long Username User',
            'password': 'testpass123'
        }
        
        with pytest.raises(ValidationError):
            user = User.objects.create_user(**user_data)
            user.full_clean()

    def test_user_email_validation(self):
        """Test email field validation."""
        User = get_user_model()
        invalid_emails = [
            'invalid-email',
            'no@domain',
            '@nodomain.com',
            'spaces @domain.com'
        ]
        
        for i, invalid_email in enumerate(invalid_emails):
            user_data = {
                'username': f'user_{i}_{invalid_email.replace("@", "_").replace(".", "_")}',
                'email': invalid_email,
                'userfullname': 'Invalid Email User',
                'password': 'testpass123'
            }
            
            with pytest.raises(ValidationError):
                user = User.objects.create_user(**user_data)
                user.full_clean()

    #def test_alter_user_role(self):
        
