import pytest


def get_user_model():
    """Get the User model after Django is configured."""
    from django.contrib.auth import get_user_model as django_get_user_model
    return django_get_user_model()


def get_user_serializers():
    """Get the serializers after Django is configured."""
    from api.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer
    return UserSerializer, UserCreateSerializer, UserUpdateSerializer


@pytest.mark.django_db
class TestUserSerializer:
    """Test cases for the UserSerializer."""

    def test_user_serializer_fields(self, test_user):
        """Test that UserSerializer includes all expected fields."""
        UserSerializer, _, _ = get_user_serializers()
        serializer = UserSerializer(test_user)
        data = serializer.data
        
        expected_fields = {'id', 'email', 'username', 'userfullname', 'role'}
        assert set(data.keys()) == expected_fields

    def test_user_serializer_read_only_fields(self, test_user):
        """Test that UserSerializer has correct read-only fields."""
        UserSerializer, _, _ = get_user_serializers()
        serializer = UserSerializer(test_user)
        
        # id should be read-only
        assert 'id' in serializer.fields
        assert serializer.fields['id'].read_only is True

    def test_user_serializer_data_accuracy(self, test_user):
        """Test that UserSerializer returns accurate data."""
        UserSerializer, _, _ = get_user_serializers()
        serializer = UserSerializer(test_user)
        data = serializer.data
        
        assert data['id'] == test_user.id
        assert data['username'] == test_user.username
        assert data['email'] == test_user.email
        assert data['userfullname'] == test_user.userfullname
        assert data['role'] == test_user.role


@pytest.mark.django_db
class TestUserCreateSerializer:
    """Test cases for the UserCreateSerializer."""

    def test_user_create_serializer_fields(self):
        """Test that UserCreateSerializer includes all expected fields."""
        _, UserCreateSerializer, _ = get_user_serializers()
        serializer = UserCreateSerializer()
        data = serializer.data
        
        expected_fields = {'email', 'username', 'userfullname', 'role', 'password'}
        assert set(data.keys()) == expected_fields

    def test_user_create_serializer_password_write_only(self):
        """Test that password field is write-only."""
        _, UserCreateSerializer, _ = get_user_serializers()
        serializer = UserCreateSerializer()
        
        assert 'password' in serializer.fields
        assert serializer.fields['password'].write_only is True

    def test_user_create_serializer_create_user(self, test_user_data):
        """Test that UserCreateSerializer creates a user correctly."""
        _, UserCreateSerializer, _ = get_user_serializers()
        serializer = UserCreateSerializer(data=test_user_data)
        
        assert serializer.is_valid()
        
        user = serializer.save()
        
        assert user.username == test_user_data['username']
        assert user.email == test_user_data['email']
        assert user.userfullname == test_user_data['userfullname']
        assert user.role == test_user_data['role']
        assert user.check_password(test_user_data['password'])

    def test_user_create_serializer_validation_required_fields(self):
        """Test that UserCreateSerializer validates required fields."""
        _, UserCreateSerializer, _ = get_user_serializers()
        # Missing required fields
        incomplete_data = {
            'username': 'testuser',
            'password': 'testpass123'
            # Missing email and userfullname
        }
        
        serializer = UserCreateSerializer(data=incomplete_data)
        assert not serializer.is_valid()
        
        # Check that appropriate errors are raised
        assert 'email' in serializer.errors
        # userfullname is optional (blank=True in model), so it shouldn't be in errors
        assert 'userfullname' not in serializer.errors

    def test_user_create_serializer_validation_email_format(self):
        """Test that UserCreateSerializer validates email format."""
        _, UserCreateSerializer, _ = get_user_serializers()
        invalid_email_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'userfullname': 'Test User',
            'password': 'testpass123'
        }
        
        serializer = UserCreateSerializer(data=invalid_email_data)
        assert not serializer.is_valid()
        assert 'email' in serializer.errors

    def test_user_create_serializer_validation_password_required(self):
        """Test that UserCreateSerializer requires password."""
        _, UserCreateSerializer, _ = get_user_serializers()
        no_password_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'userfullname': 'Test User'
            # Missing password
        }
        
        serializer = UserCreateSerializer(data=no_password_data)
        assert not serializer.is_valid()
        assert 'password' in serializer.errors


@pytest.mark.django_db
class TestUserUpdateSerializer:
    """Test cases for the UserUpdateSerializer."""

    def test_user_update_serializer_fields(self):
        """Test that UserUpdateSerializer includes only updatable fields."""
        _, _, UserUpdateSerializer = get_user_serializers()
        serializer = UserUpdateSerializer()
        data = serializer.data
        
        expected_fields = {'username', 'userfullname', 'role'}
        assert set(data.keys()) == expected_fields

    def test_user_update_serializer_excludes_sensitive_fields(self):
        """Test that UserUpdateSerializer excludes sensitive fields."""
        _, _, UserUpdateSerializer = get_user_serializers()
        serializer = UserUpdateSerializer()
        
        # Should not include password or email
        assert 'password' not in serializer.fields
        assert 'email' not in serializer.fields
        assert 'id' not in serializer.fields

    def test_user_update_serializer_update_user(self, test_user):
        """Test that UserUpdateSerializer updates a user correctly."""
        _, _, UserUpdateSerializer = get_user_serializers()
        update_data = {
            'username': 'updateduser',
            'userfullname': 'Updated User',
            'role': 'Senior Developer'
        }
        
        serializer = UserUpdateSerializer(test_user, data=update_data, partial=True)
        
        assert serializer.is_valid()
        
        updated_user = serializer.save()
        
        assert updated_user.username == update_data['username']
        assert updated_user.userfullname == update_data['userfullname']
        assert updated_user.role == update_data['role']
        
        # Email should remain unchanged
        assert updated_user.email == test_user.email

    def test_user_update_serializer_partial_update(self, test_user):
        """Test that UserUpdateSerializer allows partial updates."""
        _, _, UserUpdateSerializer = get_user_serializers()
        # Only update username
        update_data = {
            'username': 'partialupdate'
        }
        
        serializer = UserUpdateSerializer(test_user, data=update_data, partial=True)
        
        assert serializer.is_valid()
        
        updated_user = serializer.save()
        
        # Other fields should remain unchanged
        assert updated_user.userfullname == test_user.userfullname
        assert updated_user.role == test_user.role

    def test_user_update_serializer_validation_username_required(self):
        """Test that UserUpdateSerializer validates username format."""
        _, _, UserUpdateSerializer = get_user_serializers()
        invalid_username_data = {
            'username': '',  # Empty username
            'userfullname': 'Test User',
            'role': 'Developer'
        }
        
        serializer = UserUpdateSerializer(data=invalid_username_data)
        assert not serializer.is_valid()
        assert 'username' in serializer.errors

    def test_user_update_serializer_validation_role_optional(self):
        """Test that UserUpdateSerializer allows empty role."""
        _, _, UserUpdateSerializer = get_user_serializers()
        empty_role_data = {
            'username': 'testuser',
            'userfullname': 'Test User',
            'role': ''  # Empty role should be allowed
        }
        
        serializer = UserUpdateSerializer(data=empty_role_data)
        assert serializer.is_valid()
