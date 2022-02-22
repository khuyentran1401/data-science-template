# End-to-end Customer Segmentation Project

## Tools Used in This Project
* [Prefect](https://www.prefect.io/): Orchestrate workflows - [article](https://towardsdatascience.com/orchestrate-a-data-science-project-in-python-with-prefect-e69c61a49074)
* [hydra](https://hydra.cc/): Manage configuration files - [article](https://towardsdatascience.com/introduction-to-hydra-cc-a-powerful-framework-to-configure-your-data-science-projects-ed65713a53c6)
* [Weights & Biases](https://wandb.ai/): Track and monitor experiments - [article](https://towardsdatascience.com/introduction-to-weight-biases-track-and-visualize-your-machine-learning-experiments-in-3-lines-9c9553b0f99d)
* [pre-commit plugins](https://pre-commit.com/): Automate code reviewing formatting  - [article](https://towardsdatascience.com/4-pre-commit-plugins-to-automate-code-reviewing-and-formatting-in-python-c80c6d2e9f5?sk=2388804fb174d667ee5b680be22b8b1f)
* [poetry](https://python-poetry.org/): Python dependency management - [article](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f)
* [DVC](https://dvc.org/): Data version control. - [article](https://towardsdatascience.com/introduction-to-dvc-data-version-control-tool-for-machine-learning-projects-7cb49c229fe0)
* [BentoML](https://docs.bentoml.org/en/latest/): Deploy and serve machine learning models - [article](https://towardsdatascience.com/bentoml-create-an-ml-powered-prediction-service-in-minutes-23d135d6ca76)

## Variations of This Project
- [workshop branch](https://github.com/khuyentran1401/customer_segmentation/tree/workshop) focuses on Hydra, Prefect, and Weight & Biases along with explanations.
- [bentoml_demo branch](https://github.com/khuyentran1401/customer_segmentation/tree/bentoml_demo) focuses on BentoML along with explanations.

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
make install
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




