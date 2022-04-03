.PHONY: notebook docs
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

docs:
	@echo Save the output to docs... 
	pdoc src -o docs --force --http localhost:8080

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache