# Testing Guide

This document explains how to run the unit tests for the retrospectives project.

## Prerequisites

Make sure you have all the required dependencies installed:

```bash
pip install -r requirements.txt
```

The project uses:
- **pytest** - Python testing framework
- **pytest-django** - Django integration for pytest
- **Django REST Framework test utilities** - For API testing

## Running Tests

### Option 1: Using pytest directly

From the `backend` directory:

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest api/test_models.py

# Run specific test class
pytest api/test_models.py::TestUserModel

# Run specific test method
pytest api/test_models.py::TestUserModel::test_create_user_success

# Run tests with coverage
pytest --cov=api --cov-report=html
```

### Option 2: Using the test runner script

From the `backend` directory:

```bash
python run_tests.py
```

### Option 3: Using Django's test command

From the `backend` directory:

```bash
python manage.py test
```

## Test Structure

The tests are organized into the following files:

### `conftest.py`
- Contains shared pytest fixtures
- Provides test data and common setup
- Configures test database and API clients

### `api/test_models.py`
- Tests for the User model
- Covers user creation, validation, and constraints
- Tests field validation and uniqueness constraints

### `api/test_serializers.py`
- Tests for all user serializers
- Covers serialization, deserialization, and validation
- Tests field inclusion/exclusion and validation rules

### `api/test_views.py`
- Tests for the UserViewSet API endpoints
- Covers CRUD operations (Create, Read, Update, Delete)
- Tests API responses, status codes, and data validation

## Test Categories

Tests are marked with categories for easy filtering:

- **@pytest.mark.unit** - Unit tests (fast, isolated)
- **@pytest.mark.integration** - Integration tests (slower, database)
- **@pytest.mark.slow** - Slow running tests

## Running Specific Test Categories

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

## Test Database

Tests use a separate test database that is:
- Created automatically for each test run
- Destroyed after tests complete
- Isolated from your development database

## Debugging Tests

To debug failing tests:

```bash
# Run with more verbose output
pytest -v -s

# Run a single test with debugger
pytest -s --pdb api/test_views.py::TestUserViewSet::test_create_user_success

# Run with print statements visible
pytest -s
```

## Coverage Reports

Generate coverage reports to see which code is tested:

```bash
# Install coverage
pip install coverage

# Run tests with coverage
pytest --cov=api --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Best Practices

1. **Test Isolation**: Each test should be independent and not rely on other tests
2. **Descriptive Names**: Test method names should clearly describe what they test
3. **Arrange-Act-Assert**: Structure tests with clear setup, action, and verification
4. **Test Data**: Use fixtures for common test data
5. **Cleanup**: Tests should clean up after themselves

## Example Test

```python
def test_create_user_success(self, api_client, test_user_data):
    """Test successful user creation via API."""
    url = reverse('user-list')
    response = api_client.post(url, test_user_data, format='json')
    
    # Assert response
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['username'] == test_user_data['username']
    
    # Verify database state
    user = User.objects.get(username=test_user_data['username'])
    assert user.email == test_user_data['email']
```

## Troubleshooting

### Common Issues

1. **Database errors**: Make sure Django is properly configured
2. **Import errors**: Check that you're running from the correct directory
3. **Permission errors**: Ensure you have write access to create test databases

### Getting Help

If you encounter issues:
1. Check the test output for error messages
2. Verify your Django configuration
3. Ensure all dependencies are installed
4. Check that you're running tests from the `backend` directory
