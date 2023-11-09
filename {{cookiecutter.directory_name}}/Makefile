init-env:
	pip install pipenv
	@echo Activando el entorno virtual
	export PIPENV_VENV_IN_PROJECT=1
	pipenv shell
prepare-env:
	@echo Creando entorno virtual...
	export PIPENV_VENV_IN_PROJECT=1
	pipenv shell
	@echo Instalando dependencias...
	pipenv install -r requirements.txt
create-project:
	@echo installando cookieter
	pip install cookiecutter
	@echo creando projecto desde template
	cookiecutter https://github.com/kascesar/data-science-template

create-docs:
	@echo Creando y guardando la documentacion...
	mkdir docs
	pdoc . -o docs --force\

serve-docs:
	@echo Creando la vista de la documentacion...
	pdoc .. --http localhost:8080
