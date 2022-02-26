.PHONY: notebook
.EXPORT_ALL_VARIABLES:

PREFECT__FLOWS__CHECKPOINTING = true

install: 
	@echo "Installing..."
	poetry install

activate:
	@echo "Activating virtual environment"
	poetry shell

env:
	@echo "Please set the environment variable 'PREFECT__FLOWS__CHECKPOINTING=true' to persist the output of Prefect's flow"

pull_data:
	@echo "Pulling data..."
	poetry run dvc pull

setup: activate 
install_all: install pull_data env

test:
	pytest

clean: 
	@echo "Deleting log files..."
	find . -name "*.log" -type f -not -path "./wandb/*" -delete