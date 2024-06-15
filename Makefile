# Makefile for a Python project

# Default target
.PHONY: all
all: help

# Install dependencies
.PHONY: install
install:
	@echo "Installing dependencies..."
	python3 -m pip install -r requirements.txt

# Bootstrap backend
.PHONY: bootstrap_backend
bootstrap_backend:
	@echo "Bootstrapping backend..."
	make install ; python3 ./scripts/bootstrap-backend.py

# Build layer for backend stack
.PHONY: layer_builder
layer_builder:
	@echo "Building layer for backend stack..."
	chmod +x ./scripts/layer_builder.sh ; ./scripts/layer_builder.sh

# Delete layers
.PHONY: delete_layers
delete_layers: 
	@echo "Deleting layers..."
	cd backend/layers ; rm -rf *

# Update layers
.PHONY: update_layers
update_layers:
	@echo "Updating layers..."
	make delete_layers
	make layer_builder

# deploy backend stack to AWS, with new layers
.PHONY: cdk_deploy
cdk_deploy:
	@echo "Deploying backend stack..."
	@echo "Updating layers..."
	make update_layers
	@echo "Deploying backend stack..."
	cdk deploy

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
	@echo "  layer_builder - Build and zip layer for backend stack"
	@echo "  delete_layers - Delete layers"
	@echo "  update_layers - Update layers"
	@echo "  cdk_deploy - Deploy backend stack to AWS"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run tests"
	@echo "  format     - Run formatter"
	@echo "  clean      - Clean up generated files"
	@echo "  help       - Show this help message"
