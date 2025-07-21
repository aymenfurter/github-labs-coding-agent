"""Unit tests for TodoService."""

import json
import os
import pytest
from unittest.mock import patch, mock_open
from services.todo_service import TodoService
from models.todo import TodoModel


class TestTodoService:
    """Test cases for TodoService class."""

    def test_init_with_empty_file(self, todo_service):
        """Test service initialization with no existing file."""
        assert len(todo_service.todos) == 0
        assert todo_service.next_id == 1

    def test_load_todos_file_not_exists(self, monkeypatch, temp_todo_file):
        """Test loading todos when file doesn't exist."""
        # Remove the temp file to simulate non-existence
        os.unlink(temp_todo_file)

        monkeypatch.setattr("services.todo_service.TODO_FILE", temp_todo_file)
        service = TodoService()

        assert len(service.todos) == 0
        assert service.next_id == 1

    def test_load_todos_with_data(self, monkeypatch, temp_todo_file, sample_todos):
        """Test loading todos from existing file."""
        # Write sample data to temp file
        data = {"todos": sample_todos, "next_id": 3}
        with open(temp_todo_file, "w") as f:
            json.dump(data, f)

        monkeypatch.setattr("services.todo_service.TODO_FILE", temp_todo_file)
        service = TodoService()

        assert len(service.todos) == 2
        assert service.next_id == 3
        assert service.todos[0].title == "First Todo"
        assert service.todos[1].title == "Second Todo"

    def test_load_todos_invalid_json(self, monkeypatch, temp_todo_file):
        """Test loading todos with invalid JSON."""
        # Write invalid JSON to temp file
        with open(temp_todo_file, "w") as f:
            f.write("invalid json")

        monkeypatch.setattr("services.todo_service.TODO_FILE", temp_todo_file)
        service = TodoService()

        # Should handle gracefully and start with empty list
        assert len(service.todos) == 0
        assert service.next_id == 1

    def test_save_todos(self, todo_service, temp_todo_file):
        """Test saving todos to file."""
        # Add a todo
        todo = todo_service.create_todo("Test Todo", "Test Description", "high")

        # Check file was created and contains data
        assert os.path.exists(temp_todo_file)

        with open(temp_todo_file, "r") as f:
            data = json.load(f)

        assert "todos" in data
        assert "next_id" in data
        assert len(data["todos"]) == 1
        assert data["todos"][0]["title"] == "Test Todo"
        assert data["next_id"] == 2

    @patch("builtins.open", side_effect=IOError("Permission denied"))
    def test_save_todos_io_error(self, mock_file, todo_service):
        """Test save_todos handles IOError correctly."""
        with pytest.raises(IOError):
            todo_service.save_todos()

    def test_get_all_todos_empty(self, todo_service):
        """Test getting all todos when list is empty."""
        todos = todo_service.get_all_todos()
        assert todos == []

    def test_get_all_todos_with_data(self, todo_service):
        """Test getting all todos with existing data."""
        # Create some todos
        todo1 = todo_service.create_todo("Todo 1")
        todo2 = todo_service.create_todo("Todo 2")

        todos = todo_service.get_all_todos()
        assert len(todos) == 2
        assert todos[0]["title"] == "Todo 1"
        assert todos[1]["title"] == "Todo 2"

    def test_create_todo_minimal(self, todo_service):
        """Test creating todo with minimal data."""
        todo = todo_service.create_todo("Test Todo")

        assert todo.id == 1
        assert todo.title == "Test Todo"
        assert todo.description == ""
        assert todo.priority == "medium"
        assert todo.completed is False
        assert todo.created_at is not None

    def test_create_todo_full(self, todo_service):
        """Test creating todo with all data."""
        todo = todo_service.create_todo("Test Todo", "Test Description", "high")

        assert todo.id == 1
        assert todo.title == "Test Todo"
        assert todo.description == "Test Description"
        assert todo.priority == "high"
        assert todo.completed is False

    def test_create_todo_increments_id(self, todo_service):
        """Test that creating todos increments ID correctly."""
        todo1 = todo_service.create_todo("Todo 1")
        todo2 = todo_service.create_todo("Todo 2")

        assert todo1.id == 1
        assert todo2.id == 2
        assert todo_service.next_id == 3

    def test_find_todo_by_id_exists(self, todo_service):
        """Test finding todo by ID when it exists."""
        todo = todo_service.create_todo("Test Todo")
        found_todo = todo_service.find_todo_by_id(1)

        assert found_todo is not None
        assert found_todo.id == 1
        assert found_todo.title == "Test Todo"

    def test_find_todo_by_id_not_exists(self, todo_service):
        """Test finding todo by ID when it doesn't exist."""
        found_todo = todo_service.find_todo_by_id(999)
        assert found_todo is None

    def test_update_todo_exists(self, todo_service):
        """Test updating existing todo."""
        todo = todo_service.create_todo("Original Title", "Original Description", "low")

        update_data = {
            "title": "Updated Title",
            "description": "Updated Description",
            "priority": "high",
            "completed": True,
        }

        updated_todo = todo_service.update_todo(1, update_data)

        assert updated_todo is not None
        assert updated_todo.title == "Updated Title"
        assert updated_todo.description == "Updated Description"
        assert updated_todo.priority == "high"
        assert updated_todo.completed is True

    def test_update_todo_not_exists(self, todo_service):
        """Test updating non-existent todo."""
        updated_todo = todo_service.update_todo(999, {"title": "New Title"})
        assert updated_todo is None

    def test_update_todo_partial(self, todo_service):
        """Test partial update of todo."""
        todo = todo_service.create_todo("Original Title", "Original Description", "low")

        # Only update title
        updated_todo = todo_service.update_todo(1, {"title": "Updated Title"})

        assert updated_todo.title == "Updated Title"
        assert updated_todo.description == "Original Description"  # Unchanged
        assert updated_todo.priority == "low"  # Unchanged
        assert updated_todo.completed is False  # Unchanged

    def test_delete_todo_exists(self, todo_service):
        """Test deleting existing todo."""
        todo = todo_service.create_todo("Test Todo")
        assert len(todo_service.todos) == 1

        result = todo_service.delete_todo(1)

        assert result is True
        assert len(todo_service.todos) == 0

    def test_delete_todo_not_exists(self, todo_service):
        """Test deleting non-existent todo."""
        result = todo_service.delete_todo(999)
        assert result is False

    def test_delete_todo_multiple(self, todo_service):
        """Test deleting one todo from multiple."""
        todo1 = todo_service.create_todo("Todo 1")
        todo2 = todo_service.create_todo("Todo 2")
        assert len(todo_service.todos) == 2

        result = todo_service.delete_todo(1)

        assert result is True
        assert len(todo_service.todos) == 1
        assert todo_service.todos[0].id == 2

    def test_toggle_todo_completion_exists(self, todo_service):
        """Test toggling completion status of existing todo."""
        todo = todo_service.create_todo("Test Todo")
        assert todo.completed is False

        toggled_todo = todo_service.toggle_todo_completion(1)

        assert toggled_todo is not None
        assert toggled_todo.completed is True

        # Toggle again
        toggled_todo = todo_service.toggle_todo_completion(1)
        assert toggled_todo.completed is False

    def test_toggle_todo_completion_not_exists(self, todo_service):
        """Test toggling completion status of non-existent todo."""
        toggled_todo = todo_service.toggle_todo_completion(999)
        assert toggled_todo is None

    def test_validate_form_data_valid(self, todo_service):
        """Test form data validation with valid data."""
        title, priority = todo_service.validate_form_data("Test Todo", "high")

        assert title == "Test Todo"
        assert priority == "high"

    def test_validate_form_data_strip_title(self, todo_service):
        """Test form data validation strips whitespace."""
        title, priority = todo_service.validate_form_data("  Test Todo  ", "high")

        assert title == "Test Todo"
        assert priority == "high"

    def test_validate_form_data_empty_title(self, todo_service):
        """Test form data validation with empty title."""
        title, priority = todo_service.validate_form_data("", "high")

        assert title == ""
        assert priority == "high"

    def test_validate_form_data_invalid_priority(self, todo_service):
        """Test form data validation with invalid priority."""
        title, priority = todo_service.validate_form_data("Test Todo", "invalid")

        assert title == "Test Todo"
        assert priority == "medium"  # Should default to medium

    def test_validate_form_data_none_values(self, todo_service):
        """Test form data validation with None values."""
        title, priority = todo_service.validate_form_data(None, None)

        assert title == ""
        assert priority == "medium"
