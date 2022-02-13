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
* `notebook`: consists of Jupyter Notebooks
* `tests`: consists of test files

## Set Up the Project
1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Set up the environment:
```bash
make setup
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

## Serve Machine Learning Models with BentoML

To serve the trained model, run:
```bash
bentoml serve src/bentoml_app.py:service --reload
```
To send requests to the newly started service in Python, run:
```bash
python src/predict.py
```

Details of `predict.py`:
```python
import requests

prediction = requests.post(
    "http://127.0.0.1:5000/predict",
    headers={"content-type": "application/json"},
    data='{"Income": 58138, "Recency": 58, "Complain": 0,"age": 64,"total_purchases": 25,"enrollment_years": 10,"family_size": 1}',
).text

print(prediction)
```
Output:
```bash
1
```

