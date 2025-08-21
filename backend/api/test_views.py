import pytest
from django.urls import reverse
from rest_framework import status


def get_user_model():
    """Get the User model after Django is configured."""
    from django.contrib.auth import get_user_model as django_get_user_model
    return django_get_user_model()

def delete_user(user) -> None:
    """Deleted users after succesful testing"""
    try:
        user.delete()
    except Exception:
        pass  # User might already be deleted

@pytest.mark.django_db
class TestUserViewSet:
    """Test cases for the UserViewSet."""

    def test_list_users(self, api_client):
        """Test listing all users."""
        User = get_user_model()
        # Create a test user first
        user = User.objects.create_user(
            username='listuser',
            email='list@example.com',
            userfullname='List User',
            password='listpass123'
        )
        
        try:
            url = reverse('user-list')
            response = api_client.get(url)
            
            assert response.status_code == status.HTTP_200_OK
            assert len(response.data['results']) == 1
            assert response.data['results'][0]['username'] == user.username
        finally:
            delete_user(user)
        #    # Cleanup: delete the test user
        #    try:
        #        user.delete()
        #    except Exception:
        #        pass  # User might already be deleted

    def test_create_user_success(self, api_client, test_user_data):
        """Test successful user creation via API."""
        User = get_user_model()
        url = reverse('user-list')
        response = api_client.post(url, test_user_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == test_user_data['username']
        assert response.data['email'] == test_user_data['email']
        assert response.data['userfullname'] == test_user_data['userfullname']
        assert response.data['role'] == test_user_data['role']
        
        # Verify user was actually created in database
        user = User.objects.get(username=test_user_data['username'])
        assert user.email == test_user_data['email']
        assert user.check_password(test_user_data['password'])
        
        # Cleanup: delete the created user
        try:
            user.delete()
        except Exception:
            pass  # User might already be deleted

    def test_create_user_missing_required_fields(self, api_client):
        """Test user creation with missing required fields."""
        incomplete_data = {
            'username': 'incompleteuser',
            'password': 'incompletepass123'
            # Missing email and userfullname
        }
        
        url = reverse('user-list')
        response = api_client.post(url, incomplete_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
        # userfullname is optional (blank=True in model), so it shouldn't be in errors
        assert 'userfullname' not in response.data

    def test_create_user_duplicate_username(self, api_client, test_user):
        """Test user creation with duplicate username."""
        User = get_user_model()
        duplicate_data = {
            'username': test_user.username,  # Same username
            'email': 'different@example.com',
            'userfullname': 'Different User',
            'password': 'differentpass123'
        }
        
        url = reverse('user-list')
        response = api_client.post(url, duplicate_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user_duplicate_email(self, api_client, test_user):
        """Test user creation with duplicate email."""
        User = get_user_model()
        duplicate_data = {
            'username': 'differentuser',
            'email': test_user.email,  # Same email
            'userfullname': 'Different User',
            'password': 'differentpass123'
        }
        
        url = reverse('user-list')
        response = api_client.post(url, duplicate_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_create_user_invalid_email_format(self, api_client):
        """Test user creation with invalid email format."""
        invalid_email_data = {
            'username': 'invalidemailuser',
            'email': 'invalid-email-format',
            'userfullname': 'Invalid Email User',
            'password': 'invalidpass123'
        }
        
        url = reverse('user-list')
        response = api_client.post(url, invalid_email_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_create_user_password_required(self, api_client):
        """Test user creation without password."""
        no_password_data = {
            'username': 'nopassuser',
            'email': 'nopass@example.com',
            'userfullname': 'No Pass User'
            # Missing password
        }
        
        url = reverse('user-list')
        response = api_client.post(url, no_password_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data

    def test_retrieve_user(self, api_client, test_user):
        """Test retrieving a specific user."""
        url = reverse('user-detail', kwargs={'pk': test_user.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == test_user.username
        assert response.data['email'] == test_user.email

    def test_retrieve_nonexistent_user(self, api_client):
        """Test retrieving a user that doesn't exist."""
        url = reverse('user-detail', kwargs={'pk': 99999})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_user_success(self, api_client, test_user):
        """Test successful user update via API."""
        update_data = {
            'username': 'updateduser',
            'userfullname': 'Updated User',
            'role': 'Senior Developer'
        }
        
        url = reverse('user-detail', kwargs={'pk': test_user.pk})
        response = api_client.patch(url, update_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == update_data['username']
        assert response.data['userfullname'] == update_data['userfullname']
        assert response.data['role'] == update_data['role']
        
        # Verify user was actually updated in database
        test_user.refresh_from_db()
        assert test_user.username == update_data['username']
        assert test_user.userfullname == update_data['userfullname']
        assert test_user.role == update_data['role']

    def test_update_user_partial(self, api_client, test_user):
        """Test partial user update via API."""
        # Only update username
        update_data = {
            'username': 'partialupdate'
        }
        
        url = reverse('user-detail', kwargs={'pk': test_user.pk})
        response = api_client.patch(url, update_data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == update_data['username']
        # Other fields should remain unchanged
        assert response.data['userfullname'] == test_user.userfullname
        assert response.data['role'] == test_user.role

    def test_update_user_nonexistent(self, api_client):
        """Test updating a user that doesn't exist."""
        update_data = {
            'username': 'nonexistentuser',
            'userfullname': 'Nonexistent User'
        }
        
        url = reverse('user-detail', kwargs={'pk': 99999})
        response = api_client.patch(url, update_data, format='json')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_user_invalid_data(self, api_client, test_user):
        """Test user update with invalid data."""
        invalid_data = {
            'username': '',  # Empty username
            'userfullname': 'Invalid User'
        }
        
        url = reverse('user-detail', kwargs={'pk': test_user.pk})
        response = api_client.patch(url, invalid_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_delete_user_success(self, api_client, test_user):
        """Test successful user deletion via API."""
        User = get_user_model()
        url = reverse('user-detail', kwargs={'pk': test_user.pk})
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verify user was actually deleted from database
        assert not User.objects.filter(pk=test_user.pk).exists()

    def test_delete_nonexistent_user(self, api_client):
        """Test deleting a user that doesn't exist."""
        url = reverse('user-detail', kwargs={'pk': 99999})
        response = api_client.delete(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_permissions(self, api_client):
        """Test that user endpoints are accessible without authentication."""
        # Test list endpoint
        list_url = reverse('user-list')
        list_response = api_client.get(list_url)
        assert list_response.status_code == status.HTTP_200_OK
        
        # Test create endpoint
        create_data = {
            'username': 'permissionuser',
            'email': 'permission@example.com',
            'userfullname': 'Permission User',
            'password': 'permissionpass123'
        }
        create_response = api_client.post(list_url, create_data, format='json')
        assert create_response.status_code == status.HTTP_201_CREATED

    def test_user_serializer_class_selection(self, api_client):
        """Test that the correct serializer is used for different actions."""
        User = get_user_model()

        # Create action should use UserCreateSerializer
        create_data = {
            'username': 'serializertest',
            'email': 'serializer@example.com',
            'userfullname': 'Serializer Test User',
            'role': 'Serializer test role',
            'password': 'serializerpass123'
        }
        
        url = reverse('user-list')
        response = api_client.post(url, create_data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        
        # Get user ID from response - handle different response formats
        user_id = response.data.get('id') or response.data.get('pk')
        assert user_id is not None, f"Response should contain user ID: {response.data}"
        
        # Verify the response contains the expected fields
        expected_fields = ['id', 'email', 'username', 'userfullname', 'role']
        for field in expected_fields:
            assert field in response.data, f"Response missing field: {field}"
        
        # Update action should use UserUpdateSerializer
        update_data = {
            'username': 'updatedserializer',
            'role': 'Test Role'
        }
        
        detail_url = reverse('user-detail', kwargs={'pk': user_id})
        update_response = api_client.patch(detail_url, update_data, format='json')
        assert update_response.status_code == status.HTTP_200_OK
        
        # Retrieve action should use UserSerializer
        retrieve_response = api_client.get(detail_url)
        assert retrieve_response.status_code == status.HTTP_200_OK
        assert 'id' in retrieve_response.data
        assert 'email' in retrieve_response.data
        # Confirm values have been updated
        assert 'updatedserializer' == retrieve_response.data.get('username')
        assert 'Test Role' == retrieve_response.data.get('role')

        # Cleanup step
        delete_user(User.objects.filter(id=user_id))
