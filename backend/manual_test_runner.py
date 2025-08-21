#!/usr/bin/env python
"""
Manual test runner for testing API endpoints without pytest.
This script sets up Django properly and provides helper functions for testing.
"""

import os
import sys
import django
from django.conf import settings

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'retrospectives.settings')

# Setup Django
django.setup()

from django.test import Client
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import User

def create_test_user():
    """Create a test user for authentication."""
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        userfullname='Test User',
        role='Developer',
        password='testpass123'
    )
    return user

def test_user_creation():
    """Test user creation endpoint."""
    print("🧪 Testing user creation...")
    
    # Use APIClient for REST framework testing
    api_client = APIClient()
    
    create_data = {
        'username': 'manualtest',
        'email': 'manual@example.com',
        'userfullname': 'Manual Test User',
        'role': 'Developer',
        'password': 'testpass123'
    }
    
    url = reverse('user-list')
    print(f"POST {url}")
    print(f"Data: {create_data}")
    
    try:
        response = api_client.post(url, create_data, format='json')
        print(f"✅ Status: {response.status_code}")
        print(f"Response: {response.data}")
        
        if response.status_code == 201:
            user_id = response.data.get('id') or response.data.get('pk')
            print(f"✅ User created with ID: {user_id}")
            return user_id
        else:
            print(f"❌ Failed to create user: {response.data}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_user_list():
    """Test user list endpoint."""
    print("\n🧪 Testing user list...")
    
    api_client = APIClient()
    url = reverse('user-list')
    print(f"GET {url}")
    
    try:
        response = api_client.get(url)
        print(f"✅ Status: {response.status_code}")
        print(f"Response: {response.data}")
        return response
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_user_detail(user_id):
    """Test user detail endpoint."""
    if not user_id:
        print("❌ No user ID provided for detail test")
        return
        
    print(f"\n🧪 Testing user detail for ID: {user_id}")
    
    api_client = APIClient()
    url = reverse('user-detail', kwargs={'pk': user_id})
    print(f"GET {url}")
    
    try:
        response = api_client.get(url)
        print(f"✅ Status: {response.status_code}")
        print(f"Response: {response.data}")
        return response
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_user_update(user_id):
    """Test user update endpoint."""
    if not user_id:
        print("❌ No user ID provided for update test")
        return
        
    print(f"\n🧪 Testing user update for ID: {user_id}")
    
    api_client = APIClient()
    url = reverse('user-detail', kwargs={'pk': user_id})
    
    update_data = {
        'username': 'updateduser',
        'role': 'Senior Developer'
    }
    
    print(f"PATCH {url}")
    print(f"Update data: {update_data}")
    
    try:
        response = api_client.patch(url, update_data, format='json')
        print(f"✅ Status: {response.status_code}")
        print(f"Response: {response.data}")
        return response
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def cleanup_test_user(user_id):
    """Clean up test user."""
    if not user_id:
        return
        
    try:
        user = User.objects.get(pk=user_id)
        user.delete()
        print(f"✅ Test user {user_id} cleaned up")
    except User.DoesNotExist:
        print(f"⚠️ User {user_id} already deleted")
    except Exception as e:
        print(f"❌ Error cleaning up user: {e}")

def run_all_tests():
    """Run all manual tests."""
    print("🚀 Starting manual API tests...\n")
    
    # Test user creation
    user_id = test_user_creation()
    
    # Test user list
    test_user_list()
    
    # Test user detail
    test_user_detail(user_id)
    
    # Test user update
    test_user_update(user_id)
    
    # Test user list again to see the update
    test_user_list()
    
    # Cleanup
    cleanup_test_user(user_id)
    
    print("\n✨ Manual testing completed!")

if __name__ == "__main__":
    run_all_tests()
