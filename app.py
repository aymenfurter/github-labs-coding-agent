"""Main Flask application entry point."""

import logging
from flask import Flask, jsonify

from routes.todo_routes import todo_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app():
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(todo_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors."""
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {error}")
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


app = create_app()

if __name__ == '__main__':
    logger.info("Starting Todo Manager application")
    app.run(debug=True, host='0.0.0.0', port=5000)
def save_todos():
    """Save todos to JSON file"""
    try:
        with open(TODO_FILE, 'w', encoding='utf-8') as f:
            json.dump({'todos': todos, 'next_id': next_id}, f, indent=2)
        logger.info(f"Saved {len(todos)} todos to {TODO_FILE}")
    except IOError as e:
        logger.error(f"Error saving todos: {e}")
        raise

def validate_todo_data(data, is_update=False):
    """Validate todo data and return errors if any"""
    errors = []
    
    if not is_update and (not data or 'title' not in data):
        errors.append('Title is required')
    
    title = data.get('title', '').strip()
    if title and len(title) > MAX_TITLE_LENGTH:
        errors.append(f'Title must be {MAX_TITLE_LENGTH} characters or less')
    
    description = data.get('description', '').strip()
    if description and len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(f'Description must be {MAX_DESCRIPTION_LENGTH} characters or less')
    
    priority = data.get('priority', DEFAULT_PRIORITY)
    if priority not in VALID_PRIORITIES:
        errors.append(f'Priority must be one of: {", ".join(VALID_PRIORITIES)}')
    
    return errors

def create_todo_item(title, description='', priority=DEFAULT_PRIORITY):
    """Create a new todo item with validation"""
    global next_id
    
    todo = {
        'id': next_id,
        'title': title.strip(),
        'description': description.strip(),
        'completed': False,
        'created_at': datetime.now().isoformat(),
        'priority': priority
    }
    
    next_id += 1
    return todo

def find_todo_by_id(todo_id):
    """Find todo by ID, return None if not found"""
    return next((todo for todo in todos if todo['id'] == todo_id), None)

@app.route('/')
def index():
    """Main page displaying all todos"""
    return render_template('index.html', todos=todos)

@app.route('/api/todos', methods=['GET'])
def get_todos():
    """API endpoint to get all todos"""
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def create_todo():
    """API endpoint to create a new todo"""
    try:
        data = request.get_json()
        
        # Validate input
        errors = validate_todo_data(data)
        if errors:
            return jsonify({'errors': errors}), 400
        
        # Create and save todo
        todo = create_todo_item(
            data['title'],
            data.get('description', ''),
            data.get('priority', DEFAULT_PRIORITY)
        )
        
        todos.append(todo)
        save_todos()
        
        logger.info(f"Created todo: {todo['title']}")
        return jsonify(todo), 201
        
    except Exception as e:
        logger.error(f"Error creating todo: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    """API endpoint to update a todo"""
    try:
        data = request.get_json()
        
        # Validate input
        errors = validate_todo_data(data, is_update=True)
        if errors:
            return jsonify({'errors': errors}), 400
        
        # Find and update todo
        todo = find_todo_by_id(todo_id)
        if not todo:
            return jsonify({'error': 'Todo not found'}), 404
        
        # Update fields
        if 'title' in data:
            todo['title'] = data['title'].strip()
        if 'description' in data:
            todo['description'] = data['description'].strip()
        if 'completed' in data:
            todo['completed'] = bool(data['completed'])
        if 'priority' in data:
            todo['priority'] = data['priority']
        
        save_todos()
        logger.info(f"Updated todo {todo_id}: {todo['title']}")
        return jsonify(todo)
        
    except Exception as e:
        logger.error(f"Error updating todo {todo_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    """API endpoint to delete a todo"""
    try:
        global todos
        
        initial_count = len(todos)
        todos = [todo for todo in todos if todo['id'] != todo_id]
        
        if len(todos) == initial_count:
            return jsonify({'error': 'Todo not found'}), 404
        
        save_todos()
        logger.info(f"Deleted todo {todo_id}")
        return jsonify({'message': 'Todo deleted successfully'})
        
    except Exception as e:
        logger.error(f"Error deleting todo {todo_id}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/add', methods=['POST'])
def add_todo_form():
    """Handle form submission for adding todo"""
    try:
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', DEFAULT_PRIORITY)
        
        if not title:
            logger.warning("Attempted to create todo without title")
            return redirect(url_for('index'))
        
        # Validate priority
        if priority not in VALID_PRIORITIES:
            priority = DEFAULT_PRIORITY
        
        todo = create_todo_item(title, description, priority)
        todos.append(todo)
        save_todos()
        
        logger.info(f"Created todo via form: {todo['title']}")
        
    except Exception as e:
        logger.error(f"Error adding todo via form: {e}")
    
    return redirect(url_for('index'))

@app.route('/toggle/<int:todo_id>')
def toggle_todo(todo_id):
    """Toggle todo completion status"""
    try:
        todo = find_todo_by_id(todo_id)
        if todo:
            todo['completed'] = not todo['completed']
            save_todos()
            logger.info(f"Toggled todo {todo_id}: {todo['title']}")
    except Exception as e:
        logger.error(f"Error toggling todo {todo_id}: {e}")
    
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete_todo_form(todo_id):
    """Delete todo via form action"""
    try:
        global todos
        
        initial_count = len(todos)
        todos = [todo for todo in todos if todo['id'] != todo_id]
        
        if len(todos) < initial_count:
            save_todos()
            logger.info(f"Deleted todo {todo_id} via form")
            
    except Exception as e:
        logger.error(f"Error deleting todo {todo_id} via form: {e}")
    
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    load_todos()
    app.run(debug=True, host='0.0.0.0', port=5000)
