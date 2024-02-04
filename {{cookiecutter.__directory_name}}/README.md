# {{cookiecutter.project_name}}

## Tools used in this project
* [hydra](https://hydra.cc/): Manage configuration files - [article](https://mathdatasimplified.com/stop-hard-coding-in-a-data-science-project-use-configuration-files-instead/)
* [pdoc](https://github.com/pdoc3/pdoc): Automatically create an API documentation for your project
* [pre-commit plugins](https://pre-commit.com/): Automate code reviewing formatting
{% if cookiecutter.dependency_manager == "poetry" %}
* [Poetry](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f): Dependency management - [article](https://mathdatasimplified.com/poetry-a-better-way-to-manage-python-dependencies/)
{% endif %}
{% if cookiecutter.data_version_control == "dvc" %}
* [DVC](https://dvc.org/): Data version control - [article](https://mathdatasimplified.com/introduction-to-dvc-data-version-control-tool-for-machine-learning-projects-2/)
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
{%- if cookiecutter.data_version_control == "dvc" -%}
│   ├── raw                         # raw data
│   └── raw.dvc                     # DVC file of data/raw
{%- elif cookiecutter.data_version_control == "none" -%}
│   └── raw                         # raw data
{%- endif -%}
├── docs                            # documentation for your project
{%- if cookiecutter.data_version_control == "dvc" -%}
├── dvc.yaml                        # DVC pipeline
{%- endif -%}
├── .gitignore                      # ignore files that cannot commit to Git
├── Makefile                        # store useful commands to set up the environment
├── models                          # store models
├── notebooks                       # store notebooks
{%- if cookiecutter.dependency_manager == "pip" -%}
├── pyproject.toml                  # Configure black
{%- elif cookiecutter.dependency_manager == "poetry" -%}
├── .pre-commit-config.yaml         # configurations for pre-commit
├── pyproject.toml                  # dependencies for poetry
{%- endif -%}
├── README.md                       # describe your project
├── src                             # store source code
│   ├── __init__.py                 # make src a Python module 
│   ├── process.py                  # process data before training model
│   └── train_model.py              # train model
└── tests                           # store tests
    ├── __init__.py                 # make tests a Python module 
    ├── test_process.py             # test functions for process.py
    └── test_train_model.py         # test functions for train_model.py
```

## Set up the environment

{% if cookiecutter.dependency_manager == "poetry" %}
1. Install [Poetry](https://python-poetry.org/docs/#installation)
1. Activate the virtual environment:
```bash
poetry shell
```
{% else %}
1. Create the virtual environment:
```bash
python3 -m venv venv
```
1. Activate the virtual environment:
For Linux/MacOS:
```bash
source venv/bin/activate
```
For Command Prompt:
```bash
.\venv\Scripts\activate
```
{% endif %}
1. Install dependencies:
```bash
make deps 
```

To install a new package, run:
{% if cookiecutter.dependency_manager == "poetry" %}
```bash
poetry add <package-name>
```
{% else %}
```bash
pip install <package-name>
```
{% endif %}

{% if cookiecutter.data_version_control == "dvc" %}
## Version your data
To track changes to the "data" directory, type:
```bash
dvc add data
```

This command will create the "data.dvc" file, which contains a unique identifier and the location of the data directory in the file system.

To keep track of the data associated with a particular version, commit the "data.dvc" file to Git:
```bash
git add data.dvc
git commit -m "add data"
```

To push the data to remote storage, type:
```bash
dvc push 
```
{% endif %}

## Auto-generate API documentation

To auto-generate API document for your project, run:

```bash
make docs
```
