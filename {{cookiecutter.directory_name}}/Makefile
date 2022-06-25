.PHONY: notebook docs pip

install: 
	@echo "Installing..."
	pip install -r requirements.txt

create_env:
	@echo "Creating virtual environment"
	python3 -m venv venv

activate:
	@echo "Activating virtual environment"
	cd venv && source bin/activate

setup_git:
	@echo "Setting up git"
	git init 
	git rm -r --cached 'data/raw'
	git rm -r --cached 'data/processed'
	git rm -r --cached 'data/final'
	git rm -r --cached 'models'
	pre-commit install

pull_data:
	dvc pull

setup: create_env activate install setup_git

test:
	pytest

docs_view:
	@echo View API documentation... 
	pdoc src --http localhost:8080

docs_save:
	@echo Save documentation to docs... 
	pdoc src -o docs

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache