#!/bin/bash

# Test runner script for the todo application

echo "Running Todo Application Test Suite"
echo "=================================="

# Install dependencies if needed
echo "Installing dependencies..."
pip install -r requirements.txt

# Run linting
echo -e "\nRunning linter..."
python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Run tests with coverage
echo -e "\nRunning tests with coverage..."
python -m pytest --cov=. --cov-report=term-missing --cov-report=html

# Check coverage requirement
echo -e "\nChecking coverage requirement (60%)..."
python -c "
import coverage
cov = coverage.Coverage()
cov.load()
total = cov.report()
if total < 60:
    print(f'ERROR: Coverage {total:.1f}% is below required 60%')
    exit(1)
else:
    print(f'SUCCESS: Coverage {total:.1f}% meets requirement')
"

echo -e "\nAll tests passed! ✅"