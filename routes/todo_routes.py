"""Todo route handlers."""

import logging
from flask import Blueprint, render_template, request, jsonify, redirect, url_for

from models.todo import validate_todo_data
from services.todo_service import todo_service

logger = logging.getLogger(__name__)

todo_bp = Blueprint('todo', __name__)


@todo_bp.route('/')
def index():
    """Main page displaying all todos."""
    todos = todo_service.get_all_todos()
    return render_template('index.html', todos=todos)


@todo_bp.route('/api/todos', methods=['GET'])
def get_todos():
    """API endpoint to get all todos."""
    return jsonify(todo_service.get_all_todos())


@todo_bp.route('/api/todos', methods=['POST'])
def create_todo():
    """API endpoint to create a new todo."""
    try:
        data = request.get_json()
        
        # Validate input
        errors = validate_todo_data(data)
        if errors:
            return jsonify({'errors': errors}), 400
        
        # Create todo
        todo = todo_service.create_todo(
            data['title'],
            data.get('description', ''),
            data.get('priority', 'medium')
        )
        
        return jsonify(todo.to_dict()), 201
        
    except Exception as e:
        logger.error(f"Error creating todo: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@todo_bp.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """API endpoint to update a todo."""
    try:
        data = request.get_json()
        
        # Validate input
        errors = validate_todo_data(data, is_update=True)
        if errors:
            return jsonify({'errors': errors}), 400
        
        # Update todo
        todo = todo_service.update_todo(todo_id, data)
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404
        
        return jsonify(todo.to_dict())
        
    except Exception as e:
        logger.error(f"Error updating todo {todo_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@todo_bp.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """API endpoint to delete a todo."""
    try:
        if todo_service.delete_todo(todo_id):
            return jsonify({'message': 'Todo deleted successfully'})
        else:
            return jsonify({'error': 'Todo not found'}), 404
        
    except Exception as e:
        logger.error(f"Error deleting todo {todo_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@todo_bp.route('/add', methods=['POST'])
def add_todo_form():
    """Handle form submission for adding todo."""
    try:
        title = request.form.get('title', '')
        description = request.form.get('description', '')
        priority = request.form.get('priority', 'medium')
        
        # Validate and clean data
        title, priority = todo_service.validate_form_data(title, priority)
        
        if not title:
            logger.warning("Attempted to create todo without title")
            return redirect(url_for('todo.index'))
        
        todo_service.create_todo(title, description, priority)
        
    except Exception as e:
        logger.error(f"Error adding todo via form: {e}")
    
    return redirect(url_for('todo.index'))


@todo_bp.route('/toggle/<int:todo_id>')
def toggle_todo(todo_id):
    """Toggle todo completion status."""
    try:
        todo_service.toggle_todo_completion(todo_id)
    except Exception as e:
        logger.error(f"Error toggling todo {todo_id}: {e}")
    
    return redirect(url_for('todo.index'))


@todo_bp.route('/delete/<int:todo_id>')
def delete_todo_form(todo_id):
    """Delete todo via form action."""
    try:
        todo_service.delete_todo(todo_id)
    except Exception as e:
        logger.error(f"Error deleting todo {todo_id} via form: {e}")
    
    return redirect(url_for('todo.index'))
