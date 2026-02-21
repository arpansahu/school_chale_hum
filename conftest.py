"""
Shared pytest fixtures and configuration for all tests.
"""
import pytest
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.fixture
def django_client():
    """Provide a Django test client."""
    return Client()


@pytest.fixture
def test_user(db):
    """Create and return a test user."""
    return User.objects.create_user(
        username='testuser',
        email='testuser@example.com',
        password='testpass123'
    )


@pytest.fixture
def authenticated_client(db, test_user):
    """Provide an authenticated Django test client."""
    client = Client()
    client.force_login(test_user)
    return client


@pytest.fixture
def server_url():
    """Base URL for UI tests."""
    return 'http://127.0.0.1:8013'


@pytest.fixture
def base_url():
    """Base URL for Playwright UI tests."""
    return 'http://127.0.0.1:8013'
