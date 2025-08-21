import pytest


@pytest.mark.django_db
def test_simple():
    """Simple test to verify pytest-django is working."""
    assert True


@pytest.mark.django_db
def test_django_imports():
    """Test that Django imports work."""
    from django.conf import settings
    assert hasattr(settings, 'DEBUG')


@pytest.mark.django_db
def test_user_model_import():
    """Test that we can import the User model."""
    from api.models import User
    assert User is not None
