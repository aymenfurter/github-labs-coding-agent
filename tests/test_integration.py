"""Integration tests for the todo application."""

import pytest
import json
import os
import tempfile
from unittest.mock import patch
from app import create_app


class TestTodoAppIntegration:
    """Integration tests for the complete todo application."""
    
    @pytest.fixture
    def app(self):
        """Create app with test configuration."""
        app = create_app()
        app.config['TESTING'] = True
        return app
    
    @pytest.fixture
    def client(self, app):
        """Test client for the Flask application."""
        return app.test_client()
    
    @pytest.fixture
    def temp_file(self):
        """Temporary file for testing."""
        temp_fd, temp_path = tempfile.mkstemp(suffix='.json')
        os.close(temp_fd)
        yield temp_path
        if os.path.exists(temp_path):
            os.unlink(temp_path)
    
    def test_complete_todo_workflow_api(self, client, temp_file):
        """Test complete todo workflow using API endpoints."""
        with patch('services.todo_service.TODO_FILE', temp_file):
            # Reset the service
            from services.todo_service import todo_service
            todo_service.todos = []
            todo_service.next_id = 1
            
            # 1. Create a todo
            create_data = {
                'title': 'Test Todo',
                'description': 'Test Description',
                'priority': 'high'
            }
            response = client.post('/api/todos', json=create_data)
            assert response.status_code == 201
            todo = response.get_json()
            todo_id = todo['id']
            assert todo['title'] == 'Test Todo'
            assert todo['completed'] is False
            
            # 2. Get all todos
            response = client.get('/api/todos')
            assert response.status_code == 200
            todos = response.get_json()
            assert len(todos) == 1
            assert todos[0]['title'] == 'Test Todo'
            
            # 3. Update the todo
            update_data = {
                'title': 'Updated Todo',
                'completed': True
            }
            response = client.put(f'/api/todos/{todo_id}', json=update_data)
            assert response.status_code == 200
            updated_todo = response.get_json()
            assert updated_todo['title'] == 'Updated Todo'
            assert updated_todo['completed'] is True
            
            # 4. Delete the todo
            response = client.delete(f'/api/todos/{todo_id}')
            assert response.status_code == 200
            
            # 5. Verify it's deleted
            response = client.get('/api/todos')
            assert response.status_code == 200
            todos = response.get_json()
            assert len(todos) == 0
    
    def test_complete_todo_workflow_forms(self, client, temp_file):
        """Test complete todo workflow using form endpoints."""
        with patch('services.todo_service.TODO_FILE', temp_file):
            # Reset the service
            from services.todo_service import todo_service
            todo_service.todos = []
            todo_service.next_id = 1
            
            # 1. Add todo via form
            form_data = {
                'title': 'Form Todo',
                'description': 'Form Description',
                'priority': 'medium'
            }
            response = client.post('/add', data=form_data)
            assert response.status_code == 302  # Redirect
            
            # 2. Check todo was created via API
            response = client.get('/api/todos')
            assert response.status_code == 200
            todos = response.get_json()
            assert len(todos) == 1
            todo_id = todos[0]['id']
            
            # 3. Toggle completion
            response = client.get(f'/toggle/{todo_id}')
            assert response.status_code == 302  # Redirect
            
            # 4. Verify completion status changed
            response = client.get('/api/todos')
            todos = response.get_json()
            assert todos[0]['completed'] is True
            
            # 5. Delete via form
            response = client.get(f'/delete/{todo_id}')
            assert response.status_code == 302  # Redirect
            
            # 6. Verify deletion
            response = client.get('/api/todos')
            todos = response.get_json()
            assert len(todos) == 0
    
    def test_validation_errors(self, client):
        """Test validation error handling."""
        # Test empty title
        response = client.post('/api/todos', json={})
        assert response.status_code == 400
        errors = response.get_json()['errors']
        assert 'Title is required' in errors
        
        # Test invalid priority
        response = client.post('/api/todos', json={
            'title': 'Valid Title',
            'priority': 'invalid'
        })
        assert response.status_code == 400
        errors = response.get_json()['errors']
        assert any('Priority must be one of' in error for error in errors)
        
        # Test title too long
        response = client.post('/api/todos', json={
            'title': 'x' * 201
        })
        assert response.status_code == 400
        errors = response.get_json()['errors']
        assert any('Title must be 200 characters or less' in error for error in errors)
    
    def test_error_handling(self, client):
        """Test error handling for non-existent resources."""
        # Test updating non-existent todo
        response = client.put('/api/todos/999', json={'title': 'New Title'})
        assert response.status_code == 404
        assert response.get_json()['error'] == 'Todo not found'
        
        # Test deleting non-existent todo
        response = client.delete('/api/todos/999')
        assert response.status_code == 404
        assert response.get_json()['error'] == 'Todo not found'
        
        # Test 404 for non-existent routes
        response = client.get('/nonexistent')
        assert response.status_code == 404
        assert response.get_json()['error'] == 'Not found'
    
    def test_persistence(self, client, temp_file):
        """Test that todos are persisted to file."""
        with patch('services.todo_service.TODO_FILE', temp_file):
            # Reset the service
            from services.todo_service import todo_service
            todo_service.todos = []
            todo_service.next_id = 1
            
            # Create a todo
            response = client.post('/api/todos', json={
                'title': 'Persistent Todo',
                'description': 'Should be saved'
            })
            assert response.status_code == 201
            
            # Check file was created and contains data
            assert os.path.exists(temp_file)
            with open(temp_file, 'r') as f:
                data = json.load(f)
            
            assert len(data['todos']) == 1
            assert data['todos'][0]['title'] == 'Persistent Todo'
            assert data['next_id'] == 2