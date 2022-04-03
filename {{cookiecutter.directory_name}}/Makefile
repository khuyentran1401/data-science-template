.PHONY: notebook
.EXPORT_ALL_VARIABLES:

install: 
	@echo "Installing..."
	poetry install
	poetry run pre-commit install

activate:
	@echo "Activating virtual environment"
	poetry shell

initialize_git:
	git init 

pull_data:
	poetry run dvc pull

setup: initialize_git install

test:
	pytest

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	rm -rf __pycache__ .pytest_cache