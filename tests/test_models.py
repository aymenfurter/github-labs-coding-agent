"""Unit tests for TodoModel and validation functions."""

import pytest
from datetime import datetime
from models.todo import TodoModel, validate_todo_data, DEFAULT_PRIORITY, VALID_PRIORITIES, MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH


class TestTodoModel:
    """Test cases for TodoModel class."""
    
    def test_todo_model_creation_basic(self):
        """Test basic todo model creation."""
        todo = TodoModel(1, "Test Task")
        
        assert todo.id == 1
        assert todo.title == "Test Task"
        assert todo.description == ""
        assert todo.priority == DEFAULT_PRIORITY
        assert todo.completed is False
        assert todo.created_at is not None
    
    def test_todo_model_creation_full(self):
        """Test todo model creation with all parameters."""
        created_at = "2023-01-01T12:00:00"
        todo = TodoModel(
            todo_id=5,
            title="  Test Task  ",  # Should be stripped
            description="  Test Description  ",  # Should be stripped
            priority="high",
            completed=True,
            created_at=created_at
        )
        
        assert todo.id == 5
        assert todo.title == "Test Task"
        assert todo.description == "Test Description"
        assert todo.priority == "high"
        assert todo.completed is True
        assert todo.created_at == created_at
    
    def test_todo_model_to_dict(self):
        """Test converting todo model to dictionary."""
        todo = TodoModel(1, "Test Task", "Test Description", "high", True)
        todo_dict = todo.to_dict()
        
        expected_keys = {'id', 'title', 'description', 'completed', 'created_at', 'priority'}
        assert set(todo_dict.keys()) == expected_keys
        assert todo_dict['id'] == 1
        assert todo_dict['title'] == "Test Task"
        assert todo_dict['description'] == "Test Description"
        assert todo_dict['priority'] == "high"
        assert todo_dict['completed'] is True
    
    def test_todo_model_from_dict(self):
        """Test creating todo model from dictionary."""
        data = {
            'id': 3,
            'title': 'Test Todo',
            'description': 'Test Description',
            'priority': 'low',
            'completed': False,
            'created_at': '2023-01-01T12:00:00'
        }
        
        todo = TodoModel.from_dict(data)
        
        assert todo.id == 3
        assert todo.title == 'Test Todo'
        assert todo.description == 'Test Description'
        assert todo.priority == 'low'
        assert todo.completed is False
        assert todo.created_at == '2023-01-01T12:00:00'
    
    def test_todo_model_from_dict_minimal(self):
        """Test creating todo model from minimal dictionary."""
        data = {
            'id': 1,
            'title': 'Test Todo'
        }
        
        todo = TodoModel.from_dict(data)
        
        assert todo.id == 1
        assert todo.title == 'Test Todo'
        assert todo.description == ""
        assert todo.priority == DEFAULT_PRIORITY
        assert todo.completed is False
        assert todo.created_at is not None


class TestValidateTodoData:
    """Test cases for validate_todo_data function."""
    
    def test_validate_todo_data_valid(self):
        """Test validation with valid data."""
        data = {
            'title': 'Valid Todo',
            'description': 'Valid description',
            'priority': 'high'
        }
        
        errors = validate_todo_data(data)
        assert errors == []
    
    def test_validate_todo_data_missing_title(self):
        """Test validation when title is missing."""
        data = {}
        errors = validate_todo_data(data)
        assert 'Title is required' in errors
        
        data = {'title': ''}
        errors = validate_todo_data(data)
        assert 'Title is required' in errors
    
    def test_validate_todo_data_missing_title_update(self):
        """Test validation when title is missing for update (should be allowed)."""
        data = {}
        errors = validate_todo_data(data, is_update=True)
        assert 'Title is required' not in errors
    
    def test_validate_todo_data_title_too_long(self):
        """Test validation when title is too long."""
        data = {
            'title': 'x' * (MAX_TITLE_LENGTH + 1)
        }
        
        errors = validate_todo_data(data)
        assert f'Title must be {MAX_TITLE_LENGTH} characters or less' in errors
    
    def test_validate_todo_data_description_too_long(self):
        """Test validation when description is too long."""
        data = {
            'title': 'Valid Title',
            'description': 'x' * (MAX_DESCRIPTION_LENGTH + 1)
        }
        
        errors = validate_todo_data(data)
        assert f'Description must be {MAX_DESCRIPTION_LENGTH} characters or less' in errors
    
    def test_validate_todo_data_invalid_priority(self):
        """Test validation with invalid priority."""
        data = {
            'title': 'Valid Title',
            'priority': 'invalid_priority'
        }
        
        errors = validate_todo_data(data)
        expected_message = f'Priority must be one of: {", ".join(VALID_PRIORITIES)}'
        assert expected_message in errors
    
    def test_validate_todo_data_multiple_errors(self):
        """Test validation with multiple errors."""
        data = {
            'title': 'x' * (MAX_TITLE_LENGTH + 1),
            'description': 'x' * (MAX_DESCRIPTION_LENGTH + 1),
            'priority': 'invalid'
        }
        
        errors = validate_todo_data(data)
        assert len(errors) == 3  # Title, description, and priority errors
    
    def test_validate_todo_data_whitespace_handling(self):
        """Test validation handles whitespace correctly."""
        data = {
            'title': '   Valid Title   ',
            'description': '   Valid Description   '
        }
        
        errors = validate_todo_data(data)
        assert errors == []
        
        # Test that empty strings after stripping are caught
        data = {
            'title': '   ',  # Only whitespace
        }
        errors = validate_todo_data(data)
        assert 'Title is required' in errors