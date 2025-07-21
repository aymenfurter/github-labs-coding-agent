"""Unit tests for todo routes."""

import json
import pytest
from unittest.mock import patch, MagicMock
from flask import url_for


class TestTodoRoutes:
    """Test cases for todo routes."""

    def test_index_route(self, client):
        """Test the index route returns the main page."""
        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_service.get_all_todos.return_value = []

            response = client.get("/")

            assert response.status_code == 200
            mock_service.get_all_todos.assert_called_once()

    def test_get_todos_api_empty(self, client):
        """Test GET /api/todos with empty todo list."""
        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_service.get_all_todos.return_value = []

            response = client.get("/api/todos")

            assert response.status_code == 200
            assert response.json == []
            mock_service.get_all_todos.assert_called_once()

    def test_get_todos_api_with_data(self, client, sample_todos):
        """Test GET /api/todos with existing todos."""
        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_service.get_all_todos.return_value = sample_todos

            response = client.get("/api/todos")

            assert response.status_code == 200
            assert response.json == sample_todos
            mock_service.get_all_todos.assert_called_once()

    def test_create_todo_api_valid(self, client, sample_todo_data):
        """Test POST /api/todos with valid data."""
        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_todo = MagicMock()
            mock_todo.to_dict.return_value = {
                **sample_todo_data,
                "id": 1,
                "completed": False,
            }
            mock_service.create_todo.return_value = mock_todo

            response = client.post(
                "/api/todos",
                data=json.dumps(sample_todo_data),
                content_type="application/json",
            )

            assert response.status_code == 201
            assert "id" in response.json
            mock_service.create_todo.assert_called_once_with(
                "Test Todo", "This is a test todo", "high"
            )

    def test_create_todo_api_invalid_data(self, client):
        """Test POST /api/todos with invalid data."""
        invalid_data = {"description": "No title provided"}

        response = client.post(
            "/api/todos", data=json.dumps(invalid_data), content_type="application/json"
        )

        assert response.status_code == 400
        assert "errors" in response.json
        assert "Title is required" in response.json["errors"]

    def test_create_todo_api_validation_errors(self, client):
        """Test POST /api/todos with validation errors."""
        invalid_data = {"title": "x" * 201, "priority": "invalid"}  # Too long

        response = client.post(
            "/api/todos", data=json.dumps(invalid_data), content_type="application/json"
        )

        assert response.status_code == 400
        assert "errors" in response.json
        assert len(response.json["errors"]) >= 2

    def test_create_todo_api_exception(self, client, sample_todo_data):
        """Test POST /api/todos handles exceptions."""
        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_service.create_todo.side_effect = Exception("Database error")

            response = client.post(
                "/api/todos",
                data=json.dumps(sample_todo_data),
                content_type="application/json",
            )

            assert response.status_code == 500
            assert response.json["error"] == "Internal server error"

    def test_update_todo_api_valid(self, client):
        """Test PUT /api/todos/<id> with valid data."""
        update_data = {"title": "Updated Title", "completed": True}

        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_todo = MagicMock()
            mock_todo.to_dict.return_value = {**update_data, "id": 1}
            mock_service.update_todo.return_value = mock_todo

            response = client.put(
                "/api/todos/1",
                data=json.dumps(update_data),
                content_type="application/json",
            )

            assert response.status_code == 200
            assert "id" in response.json
            mock_service.update_todo.assert_called_once_with(1, update_data)

    def test_update_todo_api_not_found(self, client):
        """Test PUT /api/todos/<id> when todo not found."""
        update_data = {"title": "Updated Title"}

        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_service.update_todo.return_value = None

            response = client.put(
                "/api/todos/999",
                data=json.dumps(update_data),
                content_type="application/json",
            )

            assert response.status_code == 404
            assert response.json["error"] == "Todo not found"

    def test_update_todo_api_validation_errors(self, client):
        """Test PUT /api/todos/<id> with validation errors."""
        invalid_data = {"priority": "invalid"}

        response = client.put(
            "/api/todos/1",
            data=json.dumps(invalid_data),
            content_type="application/json",
        )

        assert response.status_code == 400
        assert "errors" in response.json

    def test_update_todo_api_exception(self, client):
        """Test PUT /api/todos/<id> handles exceptions."""
        update_data = {"title": "Updated Title"}

        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_service.update_todo.side_effect = Exception("Database error")

            response = client.put(
                "/api/todos/1",
                data=json.dumps(update_data),
                content_type="application/json",
            )

            assert response.status_code == 500
            assert response.json["error"] == "Internal server error"

    def test_delete_todo_api_success(self, client):
        """Test DELETE /api/todos/<id> successful deletion."""
        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_service.delete_todo.return_value = True

            response = client.delete("/api/todos/1")

            assert response.status_code == 200
            assert response.json["message"] == "Todo deleted successfully"
            mock_service.delete_todo.assert_called_once_with(1)

    def test_delete_todo_api_not_found(self, client):
        """Test DELETE /api/todos/<id> when todo not found."""
        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_service.delete_todo.return_value = False

            response = client.delete("/api/todos/999")

            assert response.status_code == 404
            assert response.json["error"] == "Todo not found"

    def test_delete_todo_api_exception(self, client):
        """Test DELETE /api/todos/<id> handles exceptions."""
        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_service.delete_todo.side_effect = Exception("Database error")

            response = client.delete("/api/todos/1")

            assert response.status_code == 500
            assert response.json["error"] == "Internal server error"

    def test_add_todo_form_valid(self, client):
        """Test POST /add with valid form data."""
        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_service.validate_form_data.return_value = ("Test Todo", "high")

            response = client.post(
                "/add",
                data={
                    "title": "Test Todo",
                    "description": "Test Description",
                    "priority": "high",
                },
            )

            assert response.status_code == 302  # Redirect
            mock_service.validate_form_data.assert_called_once()
            mock_service.create_todo.assert_called_once()

    def test_add_todo_form_empty_title(self, client):
        """Test POST /add with empty title."""
        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_service.validate_form_data.return_value = ("", "medium")

            response = client.post(
                "/add",
                data={
                    "title": "",
                    "description": "Test Description",
                    "priority": "medium",
                },
            )

            assert response.status_code == 302  # Redirect
            mock_service.create_todo.assert_not_called()

    def test_add_todo_form_exception(self, client):
        """Test POST /add handles exceptions."""
        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_service.validate_form_data.side_effect = Exception("Validation error")

            response = client.post(
                "/add",
                data={
                    "title": "Test Todo",
                    "description": "Test Description",
                    "priority": "high",
                },
            )

            assert response.status_code == 302  # Still redirects on error

    def test_toggle_todo_form(self, client):
        """Test GET /toggle/<id> toggles todo completion."""
        with patch("routes.todo_routes.todo_service") as mock_service:
            response = client.get("/toggle/1")

            assert response.status_code == 302  # Redirect
            mock_service.toggle_todo_completion.assert_called_once_with(1)

    def test_toggle_todo_form_exception(self, client):
        """Test GET /toggle/<id> handles exceptions."""
        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_service.toggle_todo_completion.side_effect = Exception("Toggle error")

            response = client.get("/toggle/1")

            assert response.status_code == 302  # Still redirects on error

    def test_delete_todo_form(self, client):
        """Test GET /delete/<id> deletes todo."""
        with patch("routes.todo_routes.todo_service") as mock_service:
            response = client.get("/delete/1")

            assert response.status_code == 302  # Redirect
            mock_service.delete_todo.assert_called_once_with(1)

    def test_delete_todo_form_exception(self, client):
        """Test GET /delete/<id> handles exceptions."""
        with patch("routes.todo_routes.todo_service") as mock_service:
            mock_service.delete_todo.side_effect = Exception("Delete error")

            response = client.get("/delete/1")

            assert response.status_code == 302  # Still redirects on error
