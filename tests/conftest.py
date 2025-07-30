"""Test configuration and fixtures."""

import os
import tempfile
import pytest
from unittest.mock import patch

# Set up test environment
os.environ['FLASK_ENV'] = 'testing'

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # Import here to avoid issues with the duplicate code in app.py
    from app import create_app
    
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def temp_todo_file():
    """Create a temporary file for testing todo persistence."""
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    
    # Patch the TODO_FILE constant in the service
    with patch('services.todo_service.TODO_FILE', path):
        yield path
    
    # Clean up
    if os.path.exists(path):
        os.unlink(path)

@pytest.fixture
def clean_todo_service():
    """Provide a clean todo service instance for testing."""
    from services.todo_service import TodoService
    
    # Create a fresh service instance
    service = TodoService()
    service.todos = []
    service.next_id = 1
    
    return service