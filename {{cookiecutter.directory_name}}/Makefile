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

set_up: initialize_git install

test:
	pytest

clean: 
	@echo "Deleting log files..."
	find . -name "*.log" -type f -delete