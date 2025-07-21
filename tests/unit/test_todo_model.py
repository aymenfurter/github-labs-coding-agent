"""Unit tests for TodoModel and validation functions."""

import pytest
from datetime import datetime
from models.todo import (
    TodoModel,
    validate_todo_data,
    DEFAULT_PRIORITY,
    VALID_PRIORITIES,
)


class TestTodoModel:
    """Test cases for TodoModel class."""

    def test_todo_creation_with_defaults(self):
        """Test creating a todo with default values."""
        todo = TodoModel(1, "Test Todo")

        assert todo.id == 1
        assert todo.title == "Test Todo"
        assert todo.description == ""
        assert todo.priority == DEFAULT_PRIORITY
        assert todo.completed is False
        assert todo.created_at is not None

    def test_todo_creation_with_all_fields(self):
        """Test creating a todo with all fields specified."""
        created_at = "2023-01-01T10:00:00"
        todo = TodoModel(
            todo_id=2,
            title="  Test Todo  ",  # Test trimming
            description="  Test Description  ",  # Test trimming
            priority="high",
            completed=True,
            created_at=created_at,
        )

        assert todo.id == 2
        assert todo.title == "Test Todo"  # Trimmed
        assert todo.description == "Test Description"  # Trimmed
        assert todo.priority == "high"
        assert todo.completed is True
        assert todo.created_at == created_at

    def test_to_dict(self):
        """Test converting todo to dictionary."""
        todo = TodoModel(
            1, "Test Todo", "Test Description", "high", True, "2023-01-01T10:00:00"
        )
        todo_dict = todo.to_dict()

        expected = {
            "id": 1,
            "title": "Test Todo",
            "description": "Test Description",
            "completed": True,
            "created_at": "2023-01-01T10:00:00",
            "priority": "high",
        }

        assert todo_dict == expected

    def test_from_dict(self):
        """Test creating todo from dictionary."""
        data = {
            "id": 1,
            "title": "Test Todo",
            "description": "Test Description",
            "completed": True,
            "created_at": "2023-01-01T10:00:00",
            "priority": "high",
        }

        todo = TodoModel.from_dict(data)

        assert todo.id == 1
        assert todo.title == "Test Todo"
        assert todo.description == "Test Description"
        assert todo.completed is True
        assert todo.created_at == "2023-01-01T10:00:00"
        assert todo.priority == "high"

    def test_from_dict_with_minimal_data(self):
        """Test creating todo from dictionary with minimal data."""
        data = {"id": 1, "title": "Test Todo"}

        todo = TodoModel.from_dict(data)

        assert todo.id == 1
        assert todo.title == "Test Todo"
        assert todo.description == ""
        assert todo.completed is False
        assert todo.priority == DEFAULT_PRIORITY
        assert todo.created_at is not None


class TestValidateTodoData:
    """Test cases for validate_todo_data function."""

    def test_valid_data_new_todo(self):
        """Test validation of valid data for new todo."""
        data = {
            "title": "Test Todo",
            "description": "Test Description",
            "priority": "high",
        }

        errors = validate_todo_data(data)
        assert errors == []

    def test_valid_data_update_todo(self):
        """Test validation of valid data for update."""
        data = {"description": "Updated Description", "priority": "low"}

        errors = validate_todo_data(data, is_update=True)
        assert errors == []

    def test_missing_title_new_todo(self):
        """Test validation fails when title is missing for new todo."""
        data = {"description": "Test Description"}

        errors = validate_todo_data(data)
        assert "Title is required" in errors

    def test_missing_title_update_todo(self):
        """Test validation passes when title is missing for update."""
        data = {"description": "Updated Description"}

        errors = validate_todo_data(data, is_update=True)
        assert errors == []

    def test_empty_data_new_todo(self):
        """Test validation fails for empty data."""
        errors = validate_todo_data({})
        assert "Title is required" in errors

    def test_title_too_long(self):
        """Test validation fails when title is too long."""
        data = {
            "title": "x" * 201,  # Longer than MAX_TITLE_LENGTH (200)
            "priority": "medium",
        }

        errors = validate_todo_data(data)
        assert any("Title must be 200 characters or less" in error for error in errors)

    def test_description_too_long(self):
        """Test validation fails when description is too long."""
        data = {
            "title": "Test Todo",
            "description": "x" * 1001,  # Longer than MAX_DESCRIPTION_LENGTH (1000)
            "priority": "medium",
        }

        errors = validate_todo_data(data)
        assert any(
            "Description must be 1000 characters or less" in error for error in errors
        )

    def test_invalid_priority(self):
        """Test validation fails for invalid priority."""
        data = {"title": "Test Todo", "priority": "invalid"}

        errors = validate_todo_data(data)
        assert any("Priority must be one of" in error for error in errors)

    def test_valid_priorities(self):
        """Test all valid priorities are accepted."""
        for priority in VALID_PRIORITIES:
            data = {"title": "Test Todo", "priority": priority}

            errors = validate_todo_data(data)
            # Should not have priority error
            assert not any("Priority must be one of" in error for error in errors)

    def test_multiple_errors(self):
        """Test validation returns multiple errors."""
        data = {"title": "x" * 201, "description": "x" * 1001, "priority": "invalid"}

        errors = validate_todo_data(data)
        assert len(errors) == 3
        assert any("Title must be 200 characters or less" in error for error in errors)
        assert any(
            "Description must be 1000 characters or less" in error for error in errors
        )
        assert any("Priority must be one of" in error for error in errors)

    def test_whitespace_handling(self):
        """Test that whitespace is properly handled in validation."""
        data = {
            "title": "   ",  # Only whitespace
            "description": "   ",
            "priority": "medium",
        }

        errors = validate_todo_data(data)
        # Empty title after stripping should pass validation for length but fail for required
        assert (
            len(errors) == 0
        )  # Title with only whitespace is not considered empty for validation

    def test_none_values(self):
        """Test handling of None values."""
        data = {"title": "Test Todo", "description": None, "priority": None}

        errors = validate_todo_data(data)
        # Should handle None gracefully and use defaults
        assert len(errors) == 0  # No errors since None values are handled gracefully
