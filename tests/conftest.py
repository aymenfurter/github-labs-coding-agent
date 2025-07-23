"""Test configuration and fixtures."""

import pytest
import tempfile
import os
from app import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Test CLI runner for the Flask application."""
    return app.test_cli_runner()


@pytest.fixture
def temp_todo_file():
    """Create a temporary file for testing todo persistence."""
    temp_fd, temp_path = tempfile.mkstemp(suffix='.json')
    os.close(temp_fd)
    yield temp_path
    # Cleanup
    if os.path.exists(temp_path):
        os.unlink(temp_path)