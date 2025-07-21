"""Main Flask application entry point."""

import logging
from flask import Flask, jsonify

from routes.todo_routes import todo_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {error}")
        return jsonify({"error": "Internal server error"}), 500

    return app


app = create_app()

if __name__ == "__main__":
    logger.info("Starting Todo Manager application")
    app.run(debug=True, host="0.0.0.0", port=5000)
