# End-to-end Customer Segmentation Project

## Dataset
The data is downloaded from [Kaggle](https://www.kaggle.com/imakash3011/customer-personality-analysis).
## Tools Used in This Project
* [Prefect](https://www.prefect.io/): Orchestrate workflows
* [hydra](https://hydra.cc/): Manage configuration files
* [pre-commit plugins](https://towardsdatascience.com/4-pre-commit-plugins-to-automate-code-reviewing-and-formatting-in-python-c80c6d2e9f5?sk=2388804fb174d667ee5b680be22b8b1f): Automate code reviewing formatting 
* [poetry](https://python-poetry.org/): Python dependency management
* [DVC](https://dvc.org/): Data version control
* [BentoML](https://docs.bentoml.org/en/latest/): Deploy and serve machine learning models

## Project Structure
* `src`: consists of Python scripts
* `config`: consists of configuration files
* `data`: consists of data
* `notebook`: consists of Jupyter Notebooks
* `tests`: consists of test files

## Set Up the Project
1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Set up the environment:
```bash
make setup
source activate_env.sh
```
3. To persist the output of Prefect's flow, run 
```bash
export PREFECT__FLOWS__CHECKPOINTING=true
```

## Run the Project
To run all flows, type:
```bash
python src/main.py
```

To run the `process` flow, type:
```bash
python src/main.py flow=process
```

To run the `segment` flow, type:
```bash
python src/main.py flow=segment
```



