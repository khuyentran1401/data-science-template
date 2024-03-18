.PHONY: tests docs

deps: 
	@echo "Initializing Git..."
	git init
	
	@echo "Installing dependencies..."
	poetry install --no-root
	poetry run pre-commit install
	
tests:
	pytest

docs:
	@if [ ! -f "./docs/Makefile" ]; then \
		@echo Initiating documentation; \
		cd ./docs; sphinx-quickstart --no-sep --ext-autodoc --ext-doctest --ext-todo --ext-viewcode; \
	fi
	@echo Auto-generate API documentation... 
	cd ./docs; pwd; sphinx-apidoc -o . ../src
	@echo Generate html documentation...
	cd ./docs; pwd; make clean html
	@echo View API documentation... 
	cd ./docs/_build/html; pwd; python -m http.server