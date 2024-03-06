.PHONY: tests docs

deps: 
	@echo "Initializing Git..."
	git init
	{% if cookiecutter.dependency_manager == "poetry" %}
	@echo "Installing dependencies..."
	poetry install --no-root
	poetry run pre-commit install
	{% else %}
	@echo "Installing dependencies..."
	pip install -r requirements-dev.txt
	pre-commit install
	{% endif %}
tests:
	pytest

docs:
	@echo Save documentation to docs... 
	pdoc src -o docs --force
	@echo View API documentation... 
	pdoc src --http localhost:8080	
