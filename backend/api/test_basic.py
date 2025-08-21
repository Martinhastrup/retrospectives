import pytest


@pytest.mark.django_db
def test_basic():
    """Basic test to verify pytest-django is working."""
    assert True


@pytest.mark.django_db
def test_django_imports():
    """Test that Django imports work."""
    from django.conf import settings
    assert hasattr(settings, 'DEBUG')


@pytest.mark.django_db
def test_user_model():
    """Test that we can access the User model."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    assert User is not None
