"""Test configuration and fixtures."""

import os
import pytest
import tempfile
from app import create_app
from services.todo_service import TodoService


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        }
    )
    yield app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner."""
    return app.test_cli_runner()


@pytest.fixture
def temp_todo_file():
    """Create temporary file for testing todo persistence."""
    temp_fd, temp_path = tempfile.mkstemp(suffix=".json")
    os.close(temp_fd)
    yield temp_path
    if os.path.exists(temp_path):
        os.unlink(temp_path)


@pytest.fixture
def todo_service(temp_todo_file, monkeypatch):
    """Create TodoService instance with temporary file."""
    monkeypatch.setattr("services.todo_service.TODO_FILE", temp_todo_file)
    service = TodoService()
    yield service


@pytest.fixture
def sample_todo_data():
    """Sample todo data for testing."""
    return {
        "title": "Test Todo",
        "description": "This is a test todo",
        "priority": "high",
    }


@pytest.fixture
def sample_todos():
    """Sample todos list for testing."""
    return [
        {
            "id": 1,
            "title": "First Todo",
            "description": "First test todo",
            "completed": False,
            "priority": "high",
            "created_at": "2023-01-01T10:00:00",
        },
        {
            "id": 2,
            "title": "Second Todo",
            "description": "Second test todo",
            "completed": True,
            "priority": "medium",
            "created_at": "2023-01-02T10:00:00",
        },
    ]
