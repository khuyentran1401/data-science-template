.PHONY: tests docs

deps: 
	@echo "Initializing Git..."
	git init
	@echo "Installing dependencies..."
{%- if cookiecutter.dependency_manager == "poetry" -%}
	poetry install
	poetry run pre-commit install
{%- else -%}
	pip install -r requirements.txt
	pre-commit install
{%- endif -%}

tests:
	pytest

docs:
	@echo Save documentation to docs... 
	pdoc src -o docs --force
	@echo View API documentation... 
	pdoc src --http localhost:8080	