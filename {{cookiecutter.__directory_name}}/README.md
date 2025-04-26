# {{cookiecutter.project_name}}

## Tools used in this project

* [hydra](https://hydra.cc/): Manage configuration files - [article](https://mathdatasimplified.com/stop-hard-coding-in-a-data-science-project-use-configuration-files-instead/)
* [pdoc](https://github.com/pdoc3/pdoc): Automatically create an API documentation for your project
* [pre-commit plugins](https://pre-commit.com/): Automate code reviewing formatting
{% if cookiecutter.dependency_manager == "poetry" %}
* [Poetry](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f): Dependency management - [article](https://mathdatasimplified.com/poetry-a-better-way-to-manage-python-dependencies/)
{% elif cookiecutter.dependency_manager == "uv" %}
* [uv](https://github.com/astral-sh/uv): Ultra-fast Python package installer and resolver
{% endif %}

## Project Structure

```bash
.
├── config
│   ├── main.yaml                   # Main configuration file
│   ├── model                       # Configurations for training model
│   │   ├── model1.yaml             # First variation of parameters to train model
│   │   └── model2.yaml             # Second variation of parameters to train model
│   └── process                     # Configurations for processing data
│       ├── process1.yaml           # First variation of parameters to process data
│       └── process2.yaml           # Second variation of parameters to process data
├── data
│   ├── final                       # data after training the model
│   ├── processed                   # data after processing
│   └── raw                         # raw data
├── docs                            # documentation for your project
├── .gitignore                      # ignore files that cannot commit to Git
├── models                          # store models
├── notebooks                       # store notebooks
{% if cookiecutter.dependency_manager == "pip" -%}
├── pyproject.toml                  # Configure black
{% elif cookiecutter.dependency_manager == "poetry" -%}
├── .pre-commit-config.yaml         # configurations for pre-commit
├── pyproject.toml                  # dependencies for poetry
{%- elif cookiecutter.dependency_manager == "uv" -%}
├── .pre-commit-config.yaml         # configurations for pre-commit
├── .python-version                 # specify Python version for the project
├── pyproject.toml                  # project metadata and dependencies
{%- endif %}
├── README.md                       # describe your project
├── src                             # store source code
│   ├── __init__.py                 # make src a Python module
│   ├── process.py                  # process data before training model
│   ├── train_model.py              # train model
│   └── utils.py                    # store helper functions
└── tests                           # store tests
    ├── __init__.py                 # make tests a Python module
    ├── test_process.py             # test functions for process.py
    └── test_train_model.py         # test functions for train_model.py
```

## Version Control Setup

1. Initialize Git in your project directory:
```bash
git init
```

2. Add your remote repository:
```bash
# For HTTPS
git remote add origin https://github.com/username/repository-name.git

# For SSH
git remote add origin git@github.com:username/repository-name.git
```

3. Create and switch to a new branch:
```bash
git checkout -b main
```

4. Add and commit your files:
```bash
git add .
git commit -m "Initial commit"
```

5. Push to your remote repository:
```bash
git push -u origin main
```

## Set up the environment

{% if cookiecutter.dependency_manager == "poetry" %}
1. Install [Poetry](https://python-poetry.org/docs/#installation)

2. Activate the virtual environment:

```bash
poetry shell
```

3. Install dependencies:

- To install all dependencies from pyproject.toml, run:

```bash
poetry install
```

- To install only production dependencies, run:

```bash
poetry install --only main
```

- To install a new package, run:

```bash
poetry add <package-name>
```

4. Run Python scripts:

```bash
# Run directly with poetry
poetry run python src/process.py

# Or after activating the virtual environment
python src/process.py
```
{% elif cookiecutter.dependency_manager == "uv" %}
1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)

2. Install dependencies:

- To install all dependencies from pyproject.toml, run:

```bash
uv sync
```

- To install only production dependencies, run:

```bash
uv sync --no-dev
```

- To install a new package, run:

```bash
uv add <package-name>
```

3. Run Python scripts:

```bash
uv run src/process.py
```
{% else %}
1. Create the virtual environment:

```bash
python3 -m venv venv
```

2. Activate the virtual environment:

* For Linux/MacOS:

```bash
source venv/bin/activate
```

* For Command Prompt:

```bash
.\venv\Scripts\activate
```

3. Install dependencies:

- To install all dependencies, run:

```bash
pip install -r requirements-dev.txt
```

- To install only production dependencies, run:

```bash
pip install -r requirements.txt
```

- To install a new package, run:

```bash
pip install <package-name>
```

4. Run Python scripts:

```bash
# After activating the virtual environment
python src/process.py
```
{% endif %}

## Set up pre-commit hooks

{% if cookiecutter.dependency_manager == "poetry" %}
Set up pre-commit:
```bash
poetry run pre-commit install
```

{% elif cookiecutter.dependency_manager == "uv" %}
Set up pre-commit:
```bash
uv run pre-commit install
```

{% else %}
Set up pre-commit:
```bash
pre-commit install
```

{% endif %}

The pre-commit configuration is already set up in `.pre-commit-config.yaml`. This includes:
* `ruff`: A fast Python linter and code formatter that will automatically fix issues when possible
* `black`: Python code formatting to ensure consistent code style
* `mypy`: Static type checking for Python to catch type-related errors before runtime

Pre-commit will now run automatically on every commit. If any checks fail, the commit will be aborted and the issues will be automatically fixed when possible.

## View and alter configurations

The project uses Hydra to manage configurations. You can view and modify these configurations from the command line.

To view available configurations:

{% if cookiecutter.dependency_manager == "poetry" %}
```bash
poetry run python src/process.py --help
```
{% elif cookiecutter.dependency_manager == "uv" %}
```bash
uv run src/process.py --help
```
{% else %}
```bash
python src/process.py --help
```
{% endif %}

Output:

```yaml
process is powered by Hydra.

== Configuration groups ==
Compose your configuration from those groups (group=option)

model: model1, model2
process: process1, process2


== Config ==
Override anything in the config (foo.bar=value)

process:
  use_columns:
  - col1
  - col2
model:
  name: model1
data:
  raw: data/raw/sample.csv
  processed: data/processed/processed.csv
  final: data/final/final.csv
```

To override configurations (for example, changing the input data file):

{% if cookiecutter.dependency_manager == "poetry" %}
```bash
poetry run python src/process.py data.raw=sample2.csv
```
{% elif cookiecutter.dependency_manager == "uv" %}
```bash
uv run src/process.py data.raw=sample2.csv
```
{% else %}
```bash
python src/process.py data.raw=sample2.csv
```
{% endif %}

Output:

```
Process data using sample2.csv
Columns used: ['col1', 'col2']
```

You can override any configuration value shown in the help output. Multiple overrides can be combined in a single command. For more information about Hydra's configuration system, visit the [official documentation](https://hydra.cc/docs/intro/).

## Auto-generate API documentation

{% if cookiecutter.dependency_manager == "poetry" %}
Generate static documentation:
```bash
poetry run pdoc src -o docs
```

Start documentation server (available at http://localhost:8080):
```bash
poetry run pdoc src --http localhost:8080
```
{% elif cookiecutter.dependency_manager == "uv" %}
Generate static documentation:
```bash
uv run pdoc src -o docs
```

Start documentation server (available at http://localhost:8080):
```bash
uv run pdoc src --http localhost:8080
```
{% else %}
Generate static documentation:
```bash
pdoc src -o docs
```

Start documentation server (available at http://localhost:8080):
```bash
pdoc src --http localhost:8080
```
{% endif %}

The documentation will be generated from your docstrings and type hints in your Python files. The static documentation will be saved in the `docs` directory, while the live server allows you to view the documentation with hot-reloading as you make changes.
