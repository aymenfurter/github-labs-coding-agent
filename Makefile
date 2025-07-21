.PHONY: help install test test-unit test-integration lint format clean coverage run

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Install dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:  ## Run all tests
	python -m pytest tests/ -v

test-unit:  ## Run unit tests
	python -m pytest tests/unit/ -v

test-integration:  ## Run integration tests
	python -m pytest tests/integration/ -v

lint:  ## Run linting
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

format:  ## Format code with black
	black .

format-check:  ## Check code formatting
	black --check --diff .

coverage:  ## Run tests with coverage
	python -m pytest tests/ --cov=. --cov-report=html --cov-report=term-missing

clean:  ## Clean up generated files
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf todos.json
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

run:  ## Run the application
	python app.py

dev:  ## Run in development mode
	FLASK_ENV=development python app.py