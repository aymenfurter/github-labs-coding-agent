"""Unit tests for todo models."""

import pytest
from datetime import datetime
from models.todo import TodoModel, validate_todo_data, DEFAULT_PRIORITY, VALID_PRIORITIES, MAX_TITLE_LENGTH, MAX_DESCRIPTION_LENGTH


class TestTodoModel:
    """Test TodoModel class."""
    
    def test_create_basic_todo(self):
        """Test creating a basic todo."""
        todo = TodoModel(1, "Test Todo")
        
        assert todo.id == 1
        assert todo.title == "Test Todo"
        assert todo.description == ""
        assert todo.priority == DEFAULT_PRIORITY
        assert todo.completed is False
        assert todo.created_at is not None
    
    def test_create_todo_with_all_fields(self):
        """Test creating a todo with all fields."""
        created_at = "2023-01-01T12:00:00"
        todo = TodoModel(
            todo_id=5,
            title="Complete Task",
            description="This is a test description",
            priority="high",
            completed=True,
            created_at=created_at
        )
        
        assert todo.id == 5
        assert todo.title == "Complete Task"
        assert todo.description == "This is a test description"
        assert todo.priority == "high"
        assert todo.completed is True
        assert todo.created_at == created_at
    
    def test_title_stripped(self):
        """Test that title is stripped of whitespace."""
        todo = TodoModel(1, "  Test Todo  ")
        assert todo.title == "Test Todo"
    
    def test_description_stripped(self):
        """Test that description is stripped of whitespace."""
        todo = TodoModel(1, "Test", "  Test description  ")
        assert todo.description == "Test description"
    
    def test_to_dict(self):
        """Test converting todo to dictionary."""
        todo = TodoModel(1, "Test Todo", "Test description", "high", True)
        todo_dict = todo.to_dict()
        
        expected_keys = {'id', 'title', 'description', 'completed', 'created_at', 'priority'}
        assert set(todo_dict.keys()) == expected_keys
        assert todo_dict['id'] == 1
        assert todo_dict['title'] == "Test Todo"
        assert todo_dict['description'] == "Test description"
        assert todo_dict['priority'] == "high"
        assert todo_dict['completed'] is True
    
    def test_from_dict_minimal(self):
        """Test creating todo from minimal dictionary."""
        data = {'id': 2, 'title': 'From Dict'}
        todo = TodoModel.from_dict(data)
        
        assert todo.id == 2
        assert todo.title == 'From Dict'
        assert todo.description == ''
        assert todo.priority == DEFAULT_PRIORITY
        assert todo.completed is False
    
    def test_from_dict_complete(self):
        """Test creating todo from complete dictionary."""
        data = {
            'id': 3,
            'title': 'Complete Todo',
            'description': 'Full description',
            'priority': 'low',
            'completed': True,
            'created_at': '2023-01-01T12:00:00'
        }
        todo = TodoModel.from_dict(data)
        
        assert todo.id == 3
        assert todo.title == 'Complete Todo'
        assert todo.description == 'Full description'
        assert todo.priority == 'low'
        assert todo.completed is True
        assert todo.created_at == '2023-01-01T12:00:00'


class TestValidateTodoData:
    """Test validate_todo_data function."""
    
    def test_valid_data_create(self):
        """Test validation with valid data for creation."""
        data = {
            'title': 'Valid Todo',
            'description': 'Valid description',
            'priority': 'medium'
        }
        errors = validate_todo_data(data)
        assert errors == []
    
    def test_valid_data_update(self):
        """Test validation with valid data for update."""
        data = {
            'description': 'Updated description',
            'priority': 'high'
        }
        errors = validate_todo_data(data, is_update=True)
        assert errors == []
    
    def test_missing_title_create(self):
        """Test validation fails when title is missing for creation."""
        data = {'description': 'Test description'}
        errors = validate_todo_data(data)
        assert 'Title is required' in errors
    
    def test_empty_data_create(self):
        """Test validation fails with empty data for creation."""
        errors = validate_todo_data({})
        assert 'Title is required' in errors
    
    def test_none_data_create(self):
        """Test validation fails with None data for creation."""
        errors = validate_todo_data(None)
        assert 'Title is required' in errors
    
    def test_missing_title_update_allowed(self):
        """Test validation allows missing title for update."""
        data = {'description': 'Updated description'}
        errors = validate_todo_data(data, is_update=True)
        assert errors == []
    
    def test_title_too_long(self):
        """Test validation fails when title is too long."""
        long_title = 'x' * (MAX_TITLE_LENGTH + 1)
        data = {'title': long_title}
        errors = validate_todo_data(data)
        assert f'Title must be {MAX_TITLE_LENGTH} characters or less' in errors
    
    def test_description_too_long(self):
        """Test validation fails when description is too long."""
        long_description = 'x' * (MAX_DESCRIPTION_LENGTH + 1)
        data = {
            'title': 'Valid Title',
            'description': long_description
        }
        errors = validate_todo_data(data)
        assert f'Description must be {MAX_DESCRIPTION_LENGTH} characters or less' in errors
    
    def test_invalid_priority(self):
        """Test validation fails with invalid priority."""
        data = {
            'title': 'Valid Title',
            'priority': 'invalid'
        }
        errors = validate_todo_data(data)
        assert f'Priority must be one of: {", ".join(VALID_PRIORITIES)}' in errors
    
    def test_valid_priorities(self):
        """Test validation passes with all valid priorities."""
        for priority in VALID_PRIORITIES:
            data = {
                'title': 'Valid Title',
                'priority': priority
            }
            errors = validate_todo_data(data)
            assert errors == []
    
    def test_whitespace_handling(self):
        """Test validation handles whitespace correctly."""
        data = {
            'title': '  Valid Title  ',
            'description': '  Valid description  '
        }
        errors = validate_todo_data(data)
        assert errors == []
    
    def test_multiple_errors(self):
        """Test validation returns multiple errors."""
        long_title = 'x' * (MAX_TITLE_LENGTH + 1)
        long_description = 'x' * (MAX_DESCRIPTION_LENGTH + 1)
        data = {
            'title': long_title,
            'description': long_description,
            'priority': 'invalid'
        }
        errors = validate_todo_data(data)
        
        assert len(errors) == 3
        assert any('Title must be' in error for error in errors)
        assert any('Description must be' in error for error in errors)
        assert any('Priority must be one of' in error for error in errors)


class TestConstants:
    """Test model constants."""
    
    def test_default_priority(self):
        """Test default priority is valid."""
        assert DEFAULT_PRIORITY in VALID_PRIORITIES
    
    def test_valid_priorities_not_empty(self):
        """Test valid priorities set is not empty."""
        assert len(VALID_PRIORITIES) > 0
    
    def test_max_lengths_positive(self):
        """Test max length constants are positive."""
        assert MAX_TITLE_LENGTH > 0
        assert MAX_DESCRIPTION_LENGTH > 0
        assert MAX_DESCRIPTION_LENGTH > MAX_TITLE_LENGTH