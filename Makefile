# Makefile for a Python project

# Default target
.PHONY: all
all: help

# Install dependencies
.PHONY: install
install:
	@echo "Installing dependencies..."
	python3 -m pip install -r requirements.txt

.PHONY: bootstrap_backend
bootstrap_backend:
	@echo "Bootstrapping backend..."
	make install ; python3 ./scripts/bootstrap-backend.py

# Run tests
.PHONY: test
test:
	@echo "Running tests..."
	cd ./backend/python/ ; pip install -r requirements.dev.txt ; python3 test.py

# Run formatter
.PHONY: format
format:
	@echo "Running code formatter..."
	make install ; black .

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
	@echo "  bootstrap_backend - Bootstrap backend"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run tests"
	@echo "  format     - Run formatter"
	@echo "  clean      - Clean up generated files"
	@echo "  help       - Show this help message"
