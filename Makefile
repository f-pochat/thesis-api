# Makefile for managing database migrations and running the FastAPI server

# Variables
PYTHON=python3
ALEMBIC=alembic
UVICORN=uvicorn
APP=main:app  # Change this if your FastAPI app is in a different file
MIGRATION_DIR=migrations  # Directory where your migrations are stored

# Default target
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make migrate      Run database migrations"
	@echo "  make run          Run the FastAPI server"
	@echo "  make clean        Clean up __pycache__ directories"

# Run database migrations
.PHONY: migrate
migrate:
	$(ALEMBIC) upgrade head

# Down database tables
.PHONY: down
down:
	$(ALEMBIC) downgrade

# Run the FastAPI server
.PHONY: run
run:
	$(UVICORN) $(APP) --host 0.0.0.0 --port 8080 --reload --log-level debug

# Clean up __pycache__ directories
.PHONY: clean
clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
