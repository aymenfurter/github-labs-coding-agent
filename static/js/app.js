/**
 * Todo Manager Application
 * Modern JavaScript implementation with clean code practices
 */

class TodoApp {
    constructor() {
        this.currentEditId = null;
        this.notifications = [];
        this.init();
    }

    /**
     * Initialize the application
     */
    init() {
        this.setupEventListeners();
        this.updateStats();
        this.initializeAnimations();
    }

    /**
     * Set up all event listeners
     */
    setupEventListeners() {
        // Filter functionality
        this.setupFilterButtons();
        
        // Modal functionality
        this.setupModal();
        
        // Form submissions
        this.setupForms();
        
        // Keyboard shortcuts
        this.setupKeyboardShortcuts();
    }

    /**
     * Setup filter button functionality
     */
    setupFilterButtons() {
        const filterButtons = document.querySelectorAll('.filter-btn');
        
        filterButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const filter = e.target.dataset.filter;
                this.applyFilter(filter);
                this.updateActiveFilter(e.target);
            });
        });
    }

    /**
     * Setup modal event listeners
     */
    setupModal() {
        const modal = document.getElementById('editModal');
        const closeBtn = document.querySelector('.close');
        
        if (closeBtn) {
            closeBtn.addEventListener('click', () => this.closeEditModal());
        }
        
        // Close modal on outside click
        window.addEventListener('click', (event) => {
            if (event.target === modal) {
                this.closeEditModal();
            }
        });
        
        // Close modal on escape key
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' && modal?.style.display === 'block') {
                this.closeEditModal();
            }
        });
    }

    /**
     * Setup form event listeners
     */
    setupForms() {
        const editForm = document.getElementById('editForm');
        const todoForm = document.getElementById('todo-form');
        
        if (editForm) {
            editForm.addEventListener('submit', (e) => this.handleEditSubmit(e));
        }
        
        if (todoForm) {
            todoForm.addEventListener('submit', (e) => this.handleAddTodo(e));
        }
    }

    /**
     * Setup keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (event) => {
            // Ctrl/Cmd + N to focus on new todo input
            if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
                event.preventDefault();
                const titleInput = document.getElementById('title');
                if (titleInput) {
                    titleInput.focus();
                }
            }
        });
    }

    /**
     * Apply filter to todo items
     */
    applyFilter(filter) {
        const todoItems = document.querySelectorAll('.todo-item');
        let visibleCount = 0;
        
        todoItems.forEach(item => {
            const shouldShow = this.shouldShowItem(item, filter);
            this.toggleItemVisibility(item, shouldShow);
            if (shouldShow) visibleCount++;
        });
        
        this.updateEmptyState(visibleCount === 0);
    }

    /**
     * Determine if item should be shown based on filter
     */
    shouldShowItem(item, filter) {
        const status = item.dataset.status;
        const priority = item.dataset.priority;
        
        const filterMap = {
            'all': () => true,
            'pending': () => status === 'pending',
            'completed': () => status === 'completed',
            'high': () => priority === 'high'
        };
        
        return filterMap[filter] ? filterMap[filter]() : true;
    }

    /**
     * Toggle item visibility with animation
     */
    toggleItemVisibility(item, shouldShow) {
        if (shouldShow) {
            item.classList.remove('hidden');
            item.style.animation = 'fadeIn 0.3s ease-in';
        } else {
            item.classList.add('hidden');
            item.style.animation = 'fadeOut 0.3s ease-out';
        }
    }

    /**
     * Update active filter button
     */
    updateActiveFilter(activeButton) {
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        activeButton.classList.add('active');
    }

    /**
     * Update empty state visibility
     */
    updateEmptyState(isEmpty) {
        const emptyState = document.querySelector('.empty-state');
        const todoList = document.querySelector('.todo-list');
        
        if (emptyState && todoList) {
            emptyState.style.display = isEmpty ? 'block' : 'none';
        }
    }

    /**
     * Open edit modal for todo
     */
    editTodo(id, title, description, priority) {
        this.currentEditId = id;
        
        const elements = {
            title: document.getElementById('editTitle'),
            description: document.getElementById('editDescription'),
            priority: document.getElementById('editPriority'),
            modal: document.getElementById('editModal')
        };
        
        // Validate elements exist
        if (!Object.values(elements).every(el => el)) {
            this.showNotification('Error: Modal elements not found', 'error');
            return;
        }
        
        // Set values
        elements.title.value = title;
        elements.description.value = description;
        elements.priority.value = priority;
        
        // Show modal with animation
        elements.modal.style.display = 'block';
        elements.modal.classList.add('modal-show');
        
        // Focus on title input
        setTimeout(() => elements.title.focus(), 100);
    }

    /**
     * Close edit modal
     */
    closeEditModal() {
        const modal = document.getElementById('editModal');
        if (modal) {
            modal.classList.remove('modal-show');
            setTimeout(() => {
                modal.style.display = 'none';
            }, 300);
        }
        this.currentEditId = null;
    }

    /**
     * Handle edit form submission
     */
    async handleEditSubmit(event) {
        event.preventDefault();
        
        if (!this.currentEditId) {
            this.showNotification('Error: No todo selected for editing', 'error');
            return;
        }
        
        const formData = this.getEditFormData();
        if (!this.validateFormData(formData)) {
            return;
        }
        
        try {
            await this.updateTodoAPI(this.currentEditId, formData);
            this.showNotification('Todo updated successfully!', 'success');
            this.closeEditModal();
            
            // Reload page after short delay
            setTimeout(() => window.location.reload(), 1000);
        } catch (error) {
            console.error('Error updating todo:', error);
            this.showNotification('Failed to update todo', 'error');
        }
    }

    /**
     * Get form data from edit form
     */
    getEditFormData() {
        return {
            title: document.getElementById('editTitle')?.value?.trim(),
            description: document.getElementById('editDescription')?.value?.trim(),
            priority: document.getElementById('editPriority')?.value
        };
    }

    /**
     * Validate form data
     */
    validateFormData(data) {
        if (!data.title) {
            this.showNotification('Title is required', 'error');
            return false;
        }
        
        if (data.title.length > 200) {
            this.showNotification('Title must be 200 characters or less', 'error');
            return false;
        }
        
        return true;
    }

    /**
     * Update todo via API
     */
    async updateTodoAPI(id, data) {
        const response = await fetch(`/api/todos/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to update todo');
        }
        
        return response.json();
    }

    /**
     * Handle add todo form submission
     */
    async handleAddTodo(event) {
        // For now, let the form submit normally
        // Could be enhanced to use API with better UX
        this.showNotification('Adding todo...', 'info');
    }

    /**
     * Delete todo with confirmation
     */
    async confirmDelete(id) {
        if (!confirm('Are you sure you want to delete this todo?')) {
            return;
        }
        
        try {
            await this.deleteTodoAPI(id);
            this.showNotification('Todo deleted successfully!', 'success');
            setTimeout(() => window.location.reload(), 1000);
        } catch (error) {
            console.error('Error deleting todo:', error);
            this.showNotification('Failed to delete todo', 'error');
        }
    }

    /**
     * Delete todo via API
     */
    async deleteTodoAPI(id) {
        const response = await fetch(`/api/todos/${id}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to delete todo');
        }
        
        return response.json();
    }

    /**
     * Show notification to user
     */
    showNotification(message, type = 'success') {
        const notification = this.createNotificationElement(message, type);
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Auto remove after 4 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 4000);
    }

    /**
     * Create notification DOM element
     */
    createNotificationElement(message, type) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        
        const icon = this.getNotificationIcon(type);
        notification.innerHTML = `
            <i class="fas ${icon}"></i>
            <span>${message}</span>
            <button class="notification-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        return notification;
    }

    /**
     * Get icon for notification type
     */
    getNotificationIcon(type) {
        const icons = {
            success: 'fa-check-circle',
            error: 'fa-exclamation-circle',
            info: 'fa-info-circle',
            warning: 'fa-exclamation-triangle'
        };
        return icons[type] || icons.info;
    }

    /**
     * Initialize animations and smooth scrolling
     */
    initializeAnimations() {
        // Add smooth scroll behavior
        document.documentElement.style.scrollBehavior = 'smooth';
        
        // Add intersection observer for fade-in animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);
        
        // Observe todo items
        document.querySelectorAll('.todo-item').forEach(item => {
            observer.observe(item);
        });
    }

    /**
     * Update statistics (could be enhanced for real-time updates)
     */
    updateStats() {
        // Stats are calculated server-side for now
        // This could be enhanced to update dynamically
        console.log('Stats updated');
    }
}

// Global functions for backward compatibility
let todoApp;

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    todoApp = new TodoApp();
});

// Global functions for HTML onclick handlers
function editTodo(id, title, description, priority) {
    todoApp?.editTodo(id, title, description, priority);
}

function closeEditModal() {
    todoApp?.closeEditModal();
}

function confirmDelete(id) {
    todoApp?.confirmDelete(id);
}
