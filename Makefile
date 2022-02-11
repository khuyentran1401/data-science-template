.PHONY: notebook
.EXPORT_ALL_VARIABLES:

PREFECT__FLOWS__CHECKPOINTING = true

install: 
	@echo "Installing..."
	poetry shell
	poetry install

activate:
	@echo "Activating virtual environment"
	poetry shell

env:
	@echo "Please set the environment variable 'PREFECT__FLOWS__CHECKPOINTING=true' to persist the output of Prefect's flow"

pull_data:
	@echo "Pulling data..."
	dvc pull

setup: install activate pull_data env

test:
	pytest


	
