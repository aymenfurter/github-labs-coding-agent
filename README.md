# 📋 Todo Manager

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v2.3.3-green.svg)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=flat&logo=javascript&logoColor=%23F7DF1E)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

A modern, responsive Todo Manager application built with Flask. Organize your tasks with priorities, descriptions, and real-time filtering capabilities.

## 📸 Screenshot

![Todo Manager Application](https://github.com/user-attachments/assets/f21b9a24-809a-4446-b363-d6a31c573ba7)

## ✨ Features

- **📝 Task Management**: Create, edit, and delete todos with titles and descriptions
- **🎯 Priority Levels**: Organize tasks by Low, Medium, and High priority
- **✅ Status Tracking**: Mark tasks as complete or incomplete
- **🔍 Smart Filtering**: Filter todos by status (All, Pending, Completed) and priority
- **📊 Real-time Statistics**: View total, pending, and completed task counts
- **🎨 Modern UI**: Clean, responsive design with intuitive user experience
- **🚀 RESTful API**: Full API support for programmatic access
- **📱 Mobile Friendly**: Responsive design that works on all devices

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

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
   Navigate to `http://localhost:5000` to access the Todo Manager

## 🚀 Usage

### Web Interface

1. **Adding a Todo**: Fill in the title (required), description (optional), and select a priority level, then click "Add Todo"
2. **Completing a Todo**: Click the checkmark icon to mark a task as complete/incomplete
3. **Editing a Todo**: Click the edit icon to modify the task details
4. **Deleting a Todo**: Click the trash icon to remove a task (confirmation required)
5. **Filtering**: Use the filter buttons to view specific sets of todos

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/todos` | Get all todos |
| `POST` | `/api/todos` | Create a new todo |
| `PUT` | `/api/todos/<id>` | Update a specific todo |
| `DELETE` | `/api/todos/<id>` | Delete a specific todo |

#### API Examples

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
  -d '{"completed": true}'
```

## 📁 Project Structure

```
github-labs-coding-agent/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── models/
│   ├── __init__.py
│   └── todo.py           # Todo model and validation
├── routes/
│   ├── __init__.py
│   └── todo_routes.py    # Route handlers
├── services/
│   ├── __init__.py
│   └── todo_service.py   # Business logic layer
├── templates/
│   ├── base.html         # Base template
│   └── index.html        # Main page template
├── static/
│   └── js/
│       └── app.js        # Frontend JavaScript
└── .devcontainer/        # Development container config
```

## 🏗️ Architecture

The application follows a clean architecture pattern:

- **Models**: Data models and validation logic
- **Routes**: HTTP request handlers using Flask blueprints
- **Services**: Business logic and data persistence
- **Templates**: Jinja2 templates for the frontend
- **Static Files**: CSS, JavaScript, and other assets

## 🔧 Configuration

The application uses the following default settings:

- **Host**: `0.0.0.0` (all interfaces)
- **Port**: `5000`
- **Debug Mode**: Enabled in development
- **Data Storage**: JSON file (`todos.json`)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (if available)
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Bug Reports

If you find a bug, please open an issue with:
- A clear description of the problem
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots (if applicable)

## 🚀 Future Enhancements

- [ ] User authentication and authorization
- [ ] Database integration (PostgreSQL/MySQL)
- [ ] Task categories and tags
- [ ] Due dates and reminders
- [ ] Collaborative todos (sharing)
- [ ] Dark mode theme
- [ ] Data export/import functionality
- [ ] Search functionality

---

Made with ❤️ using Flask and modern web technologies.