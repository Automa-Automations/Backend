# Makefile for a Python project

# Default target
.PHONY: all
all: help

# Install dependencies
.PHONY: install
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Run tests
.PHONY: test
test:
	@echo "Running tests..."
	python3 backend/python/test.py

# Run formatter
.PHONY: format
format:
	@echo "Running code formatter..."
	pip install -r requirements.txt ; black .

# Clean up
.PHONY: clean
clean:
	@echo "Cleaning up..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

# Help
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run tests"
	@echo "  format     - Run formatter"
	@echo "  clean      - Clean up generated files"
	@echo "  help       - Show this help message"
