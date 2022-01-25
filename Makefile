.PHONY: notebook

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

process:
	poetry run python src/process_data.py 

segment:
	poetry run python src/segment.py

notebook:
	poetry run jupyter notebook
	
