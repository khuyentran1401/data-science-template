install: 
	@echo "Installing..."
	poetry shell
	poetry install

pull_data:
	@echo "Pulling data..."
	dvc pull

startup:
	@echo "Startup"
	export PREFECT__FLOWS__CHECKPOINTING=true

setup: install startup pull_data

test:
	poetry run pytest
	
