# {{cookiecutter.directory_name}}

## Set up the environment
1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Set up the environment:
```bash
make env 
```

## Install dependencies
To install all dependencies for this project, run:
```bash
poetry install
```

To install a new package, run:
```bash
poetry add <package-name>
```

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

## Auto-generate API documentation

To auto-generate API document for your project, run:

```bash
make docs
```
