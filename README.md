# Todo Manager 📝

A modern, feature-rich Todo Manager web application built with Flask. This application provides a clean and intuitive interface for managing your daily tasks with priority levels, filtering capabilities, and a comprehensive API.

![Todo Manager Screenshot](https://github.com/user-attachments/assets/494e9211-4f31-4a8f-8a17-63d45dafdd20)

## ✨ Features

- **📋 Task Management**: Create, edit, delete, and mark todos as complete
- **🔄 Priority System**: Organize tasks with Low, Medium, and High priority levels
- **📊 Statistics Dashboard**: View total, pending, and completed task counts
- **🔍 Smart Filtering**: Filter tasks by status (All, Pending, Completed) or priority
- **💾 Data Persistence**: Automatic saving to JSON file storage
- **🎨 Modern UI**: Clean, responsive design with intuitive user experience
- **🚀 RESTful API**: Full API support for programmatic access
- **⌨️ Keyboard Shortcuts**: Enhanced productivity with keyboard navigation
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/aymenfurter/github-labs-coding-agent.git
   cd github-labs-coding-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000` to start using the Todo Manager.

## 📖 Usage Guide

### Adding a Todo
1. Fill in the **Title** field (required)
2. Optionally add a **Description**
3. Select a **Priority** level (Low, Medium, High)
4. Click **Add Todo**

### Managing Todos
- **Complete/Uncomplete**: Click the checkmark icon
- **Edit**: Click the edit icon to modify task details
- **Delete**: Click the trash icon (with confirmation)

### Filtering Todos
Use the filter buttons to view:
- **All**: Show all todos
- **Pending**: Show incomplete todos only
- **Completed**: Show completed todos only
- **High Priority**: Show high-priority todos only

## 🔌 API Documentation

The application provides a RESTful API for programmatic access:

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/todos` | Retrieve all todos |
| `POST` | `/api/todos` | Create a new todo |
| `PUT` | `/api/todos/<id>` | Update an existing todo |
| `DELETE` | `/api/todos/<id>` | Delete a todo |

### API Examples

**Get all todos:**
```bash
curl http://localhost:5000/api/todos
```

**Create a new todo:**
```bash
curl -X POST http://localhost:5000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Flask", "description": "Build a todo app", "priority": "high"}'
```

**Update a todo:**
```bash
curl -X PUT http://localhost:5000/api/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "completed": true}'
```

**Delete a todo:**
```bash
curl -X DELETE http://localhost:5000/api/todos/1
```

## 🏗️ Project Structure

```
github-labs-coding-agent/
├── app.py                 # Main Flask application entry point
├── requirements.txt       # Python dependencies
├── todos.json            # Data storage (auto-generated)
├── models/
│   ├── __init__.py
│   └── todo.py           # Todo model and validation logic
├── routes/
│   ├── __init__.py
│   └── todo_routes.py    # Route handlers for todo operations
├── services/
│   ├── __init__.py
│   └── todo_service.py   # Business logic and data operations
├── templates/
│   ├── base.html         # Base HTML template
│   └── index.html        # Main page template
├── static/
│   ├── css/
│   │   └── style.css     # Application styles
│   └── js/
│       └── app.js        # Frontend JavaScript functionality
└── .devcontainer/
    └── devcontainer.json # Development container configuration
```

## 🛠️ Development

### Architecture

The application follows a clean MVC (Model-View-Controller) architecture with these key components:

- **Models** (`models/`): Data models and validation logic
- **Routes** (`routes/`): HTTP request handlers and API endpoints
- **Services** (`services/`): Business logic and data persistence
- **Templates** (`templates/`): HTML templates with Jinja2
- **Static Assets** (`static/`): CSS, JavaScript, and other frontend resources

### Key Design Patterns

- **Service Layer Pattern**: Business logic separated from route handlers
- **Repository Pattern**: Data access abstraction with JSON file storage
- **Factory Pattern**: Application creation with configuration
- **Blueprint Pattern**: Modular route organization

### Development Environment

The project includes a `.devcontainer` configuration for consistent development environments using Docker and VS Code.

### Code Style

- **Python**: Follows PEP 8 guidelines
- **JavaScript**: Modern ES6+ syntax with clean coding practices
- **HTML/CSS**: Semantic markup with BEM methodology

## 🧪 Testing

To test the application manually:

1. Start the application: `python app.py`
2. Navigate to `http://localhost:5000`
3. Test all CRUD operations through the UI
4. Test API endpoints using curl or a REST client

## 📝 Data Storage

Todos are stored in a `todos.json` file with the following structure:

```json
{
  "todos": [
    {
      "id": 1,
      "title": "Sample Todo",
      "description": "This is a sample todo item",
      "completed": false,
      "created_at": "2024-01-01T12:00:00",
      "priority": "medium"
    }
  ],
  "next_id": 2
}
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** following the existing code style
4. **Test your changes** thoroughly
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Create a Pull Request**

### Contribution Guidelines

- Follow the existing code style and patterns
- Add comments for complex logic
- Test your changes before submitting
- Update documentation if needed
- Keep commits focused and descriptive

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🚀 Deployment

For production deployment:

1. **Use a production WSGI server** (e.g., Gunicorn)
2. **Set environment variables** for configuration
3. **Use a proper database** instead of JSON files for scalability
4. **Implement proper logging** and monitoring
5. **Add authentication** if required

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🐛 Issues and Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/aymenfurter/github-labs-coding-agent/issues) page
2. Create a new issue with detailed information
3. Include steps to reproduce the problem
4. Provide your environment details

## 🎯 Future Enhancements

Potential features for future versions:

- [ ] User authentication and authorization
- [ ] Database integration (PostgreSQL/MySQL)
- [ ] Task categories and tags
- [ ] Due dates and reminders
- [ ] File attachments
- [ ] Team collaboration features
- [ ] Export/Import functionality
- [ ] Advanced search and filtering
- [ ] Mobile app version
- [ ] Dark theme support

---

**Built with ❤️ using Flask and modern web technologies**