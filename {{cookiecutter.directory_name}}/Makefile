.PHONY: tests docs

dependencies: 
	@echo "Initializing Git..."
	git init
	@echo "Installing dependencies..."
	poetry install
	poetry run pre-commit install

env: dependencies
	@echo "Activating virtual environment..."
	poetry shell

tests:
	pytest

docs:
	@echo Save documentation to docs... 
	pdoc src -o docs
	@echo View API documentation... 
	pdoc src --http localhost:8080	