import pytest


@pytest.fixture
def api_client():
    """Return an API client for testing."""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def request_factory():
    """Return a request factory for testing."""
    from django.test import RequestFactory
    return RequestFactory()


@pytest.fixture
def test_user_data():
    """Return test data for creating a user."""
    return {
        'username': 'testuser',
        'email': 'test@example.com',
        'userfullname': 'Test User',
        'role': 'Developer',
        'password': 'testpass123'
    }


@pytest.fixture
def test_user(test_user_data):
    """Create and return a test user."""
    from api.models import User
    user = User.objects.create_user(
        username=test_user_data['username'],
        email=test_user_data['email'],
        userfullname=test_user_data['userfullname'],
        role=test_user_data['role'],
        password=test_user_data['password']
    )
    yield user
    # Cleanup after test - handle case where user might already be deleted
    try:
        if user.pk:
            user.delete()
    except Exception:
        pass  # User might already be deleted or in a bad state


@pytest.fixture
def authenticated_client(api_client, test_user):
    """Return an authenticated API client."""
    api_client.force_authenticate(user=test_user)
    return api_client
