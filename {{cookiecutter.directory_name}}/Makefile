init-env: 
	@echo "Creating env"
	pipenv shell
	@echo "Installing dependencies"
	pipenv install

env: dependencies
	@echo "Activating virtual environment..."
	pipenv shell

docs:
	@echo Save documentation to docs... 
	pdoc src -o docs --force
	@echo View API documentation... 
	pdoc src --http localhost:8080	
