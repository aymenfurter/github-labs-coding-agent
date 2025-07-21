"""Integration tests for the todo application."""

import json
import os
import tempfile
import pytest
from app import create_app
from services.todo_service import TodoService


class TestTodoAppIntegration:
    """Integration tests for the complete todo application."""

    @pytest.fixture(autouse=True)
    def setup_isolated_service(self, monkeypatch):
        """Ensure each test gets a fresh service instance."""
        # Create temporary file for each test
        import tempfile
        import os

        temp_fd, temp_path = tempfile.mkstemp(suffix=".json")
        os.close(temp_fd)

        # Patch the TODO_FILE constant
        monkeypatch.setattr("services.todo_service.TODO_FILE", temp_path)

        # Create fresh service instance
        from services.todo_service import TodoService

        fresh_service = TodoService()
        monkeypatch.setattr("services.todo_service.todo_service", fresh_service)

        yield

        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    @pytest.fixture
    def app_with_temp_storage(self):
        """Create app with temporary storage."""
        app = create_app()
        app.config.update(
            {
                "TESTING": True,
            }
        )
        yield app

    @pytest.fixture
    def client_with_temp_storage(self, app_with_temp_storage):
        """Create test client with temporary storage."""
        return app_with_temp_storage.test_client()

    def test_full_todo_lifecycle_api(self, client_with_temp_storage):
        """Test complete todo lifecycle through API."""
        client = client_with_temp_storage

        # 1. Initially no todos
        response = client.get("/api/todos")
        assert response.status_code == 200
        assert response.json == []

        # 2. Create a todo
        todo_data = {
            "title": "Test Todo",
            "description": "This is a test todo",
            "priority": "high",
        }

        response = client.post(
            "/api/todos", data=json.dumps(todo_data), content_type="application/json"
        )
        assert response.status_code == 201
        created_todo = response.json
        assert created_todo["id"] == 1
        assert created_todo["title"] == "Test Todo"
        assert created_todo["completed"] is False

        # 3. Get all todos and verify our todo exists
        response = client.get("/api/todos")
        assert response.status_code == 200
        todos = response.json
        assert len(todos) == 1
        assert todos[0]["id"] == 1

        # 4. Update the todo
        update_data = {
            "title": "Updated Test Todo",
            "completed": True,
            "priority": "low",
        }

        response = client.put(
            "/api/todos/1",
            data=json.dumps(update_data),
            content_type="application/json",
        )
        assert response.status_code == 200
        updated_todo = response.json
        assert updated_todo["title"] == "Updated Test Todo"
        assert updated_todo["completed"] is True
        assert updated_todo["priority"] == "low"

        # 5. Verify persistence by getting todos again
        response = client.get("/api/todos")
        assert response.status_code == 200
        todos = response.json
        assert len(todos) == 1
        assert todos[0]["title"] == "Updated Test Todo"
        assert todos[0]["completed"] is True

        # 6. Delete the todo
        response = client.delete("/api/todos/1")
        assert response.status_code == 200
        assert response.json["message"] == "Todo deleted successfully"

        # 7. Verify todo is deleted
        response = client.get("/api/todos")
        assert response.status_code == 200
        assert response.json == []

    def test_multiple_todos_api(self, client_with_temp_storage):
        """Test handling multiple todos through API."""
        client = client_with_temp_storage

        # Create multiple todos
        todos_data = [
            {"title": "First Todo", "priority": "high"},
            {"title": "Second Todo", "priority": "medium"},
            {"title": "Third Todo", "priority": "low"},
        ]

        created_ids = []
        for todo_data in todos_data:
            response = client.post(
                "/api/todos",
                data=json.dumps(todo_data),
                content_type="application/json",
            )
            assert response.status_code == 201
            created_ids.append(response.json["id"])

        # Verify all todos exist
        response = client.get("/api/todos")
        assert response.status_code == 200
        todos = response.json
        assert len(todos) == 3

        # Delete middle todo
        response = client.delete(f"/api/todos/{created_ids[1]}")
        assert response.status_code == 200

        # Verify correct todo was deleted
        response = client.get("/api/todos")
        assert response.status_code == 200
        todos = response.json
        assert len(todos) == 2
        assert todos[0]["title"] == "First Todo"
        assert todos[1]["title"] == "Third Todo"

    def test_todo_form_integration(self, client_with_temp_storage):
        """Test todo form submission integration."""
        client = client_with_temp_storage

        # Test form submission
        response = client.post(
            "/add",
            data={
                "title": "Form Todo",
                "description": "Created via form",
                "priority": "medium",
            },
        )
        assert response.status_code == 302  # Redirect after creation

        # Verify todo was created
        response = client.get("/api/todos")
        assert response.status_code == 200
        todos = response.json
        assert len(todos) == 1
        assert todos[0]["title"] == "Form Todo"
        assert todos[0]["description"] == "Created via form"
        assert todos[0]["priority"] == "medium"

    def test_toggle_todo_integration(self, client_with_temp_storage):
        """Test toggling todo completion through form."""
        client = client_with_temp_storage

        # Create a todo first
        todo_data = {"title": "Toggle Test Todo"}
        response = client.post(
            "/api/todos", data=json.dumps(todo_data), content_type="application/json"
        )
        assert response.status_code == 201
        todo_id = response.json["id"]

        # Initially not completed
        response = client.get("/api/todos")
        assert response.json[0]["completed"] is False

        # Toggle completion
        response = client.get(f"/toggle/{todo_id}")
        assert response.status_code == 302  # Redirect

        # Verify completion status changed
        response = client.get("/api/todos")
        assert response.json[0]["completed"] is True

        # Toggle again
        response = client.get(f"/toggle/{todo_id}")
        assert response.status_code == 302

        # Verify completion status changed back
        response = client.get("/api/todos")
        assert response.json[0]["completed"] is False

    def test_delete_todo_form_integration(self, client_with_temp_storage):
        """Test deleting todo through form."""
        client = client_with_temp_storage

        # Create a todo first
        todo_data = {"title": "Delete Test Todo"}
        response = client.post(
            "/api/todos", data=json.dumps(todo_data), content_type="application/json"
        )
        assert response.status_code == 201
        todo_id = response.json["id"]

        # Verify todo exists
        response = client.get("/api/todos")
        assert len(response.json) == 1

        # Delete via form
        response = client.get(f"/delete/{todo_id}")
        assert response.status_code == 302  # Redirect

        # Verify todo is deleted
        response = client.get("/api/todos")
        assert response.json == []

    def test_error_handling_404(self, client_with_temp_storage):
        """Test 404 error handling."""
        client = client_with_temp_storage

        # Try to update non-existent todo
        response = client.put(
            "/api/todos/999",
            data=json.dumps({"title": "Updated"}),
            content_type="application/json",
        )
        assert response.status_code == 404
        assert response.json["error"] == "Todo not found"

        # Try to delete non-existent todo
        response = client.delete("/api/todos/999")
        assert response.status_code == 404
        assert response.json["error"] == "Todo not found"

    def test_validation_errors_api(self, client_with_temp_storage):
        """Test validation error handling in API."""
        client = client_with_temp_storage

        # Missing title
        response = client.post(
            "/api/todos",
            data=json.dumps({"description": "No title"}),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert "errors" in response.json
        assert "Title is required" in response.json["errors"]

        # Invalid priority
        response = client.post(
            "/api/todos",
            data=json.dumps({"title": "Test Todo", "priority": "invalid"}),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert "errors" in response.json

    def test_data_persistence(self, client_with_temp_storage, monkeypatch):
        """Test that data persists across service instances."""
        import tempfile
        import os

        # Create specific temp file for this test
        temp_fd, temp_path = tempfile.mkstemp(suffix=".json")
        os.close(temp_fd)

        try:
            # Set up first service instance
            monkeypatch.setattr("services.todo_service.TODO_FILE", temp_path)
            from services.todo_service import TodoService

            service1 = TodoService()
            monkeypatch.setattr("services.todo_service.todo_service", service1)

            client = client_with_temp_storage

            # Create todo with first service
            todo_data = {"title": "Persistence Test"}
            response = client.post(
                "/api/todos",
                data=json.dumps(todo_data),
                content_type="application/json",
            )
            assert response.status_code == 201

            # Create second service instance (simulating restart)
            service2 = TodoService()
            monkeypatch.setattr("services.todo_service.todo_service", service2)

            # Verify data persists
            response = client.get("/api/todos")
            assert response.status_code == 200
            todos = response.json
            assert len(todos) == 1
            assert todos[0]["title"] == "Persistence Test"

        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_index_page_integration(self, client_with_temp_storage):
        """Test that index page loads correctly."""
        client = client_with_temp_storage

        # Test index page loads
        response = client.get("/")
        assert response.status_code == 200
        assert b"html" in response.data.lower()  # Basic HTML check

        # Add a todo and test page still loads
        todo_data = {"title": "Test Todo for Index"}
        client.post(
            "/api/todos", data=json.dumps(todo_data), content_type="application/json"
        )

        response = client.get("/")
        assert response.status_code == 200
