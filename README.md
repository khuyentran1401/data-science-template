[![View article](https://img.shields.io/badge/Data_Science_Simplified-View_article-blue)](https://mathdatasimplified.com/2023/06/17/how-to-structure-a-data-science-project-for-readability-and-transparency-2/) [![View on YouTube](https://img.shields.io/badge/YouTube-Watch%20on%20Youtube-red?logo=youtube)](https://youtu.be/TzvcPi3nsdw) 

# Directory templates for Data Science projects

## Why?
It is important to structure your data science project based on a certain standard so that your teammates can easily maintain and modify your project.

This repository provides a template that incorporates best practices to create a maintainable and reproducible data science project.

## Tools

| Functionality  | Tool | Links |
|   ---               |        ---   |     ---   |
| Package management |   Poetry | [🔗](https://mathdatasimplified.com/poetry-a-better-way-to-manage-python-dependencies) [🔗](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f) |
| Config file manager | Hydra | [🔗](https://mathdatasimplified.com/stop-hard-coding-in-a-data-science-project-use-configuration-files-instead) [🔗](https://hydra.cc/) |
| Data version control | Amazon S3 | [🔗](https://aws.amazon.com/s3) |

<!---
* [pre-commit plugins](https://pre-commit.com/): Automate code reviewing formatting
* [pdoc](https://github.com/pdoc3/pdoc): Automatically create an API documentation for your project
--->

## Project Structure
```bash
.
├── config
│   ├── main.yaml               # Main configuration file
│   ├── model                   # Configurations for training model
│   │   ├── model1.yaml         # First variation of parameters to train model
│   │   └── model2.yaml         # Second variation of parameters to train model
│   ├── process                 # Configurations for processing data
│   │   ├── process1.yaml       # First variation of parameters to process data
│   │   └── process2.yaml       # Second variation of parameters to process data
│   └── sagemaker_lifecycle.sh  # SageMaker lifecycle config file
├── data                        
│   ├── final                   # Data after training the model
│   ├── processed               # Data after processing
│   ├── raw                     # Raw data
├── docs                        # Documentation for your project
├── Makefile                    # Store useful commands to set up the environment
├── .gitignore                  # Ignore files that cannot commit to Git  
├── models                      # Store models
├── notebooks                   # Store notebooks
├── .pre-commit-config.yaml     # Configurations for pre-commit
├── pyproject.toml              # Dependencies for poetry
├── README.md                   # Describe your project
├── src                         # Store source code
│   ├── __init__.py             # Make src a Python module 
│   ├── process.py              # Process data before training model
│   └── train_model.py          # Train model
└── tests                       # Store tests
    ├── __init__.py             # Make tests a Python module 
    ├── test_process.py         # Test functions for process.py
    └── test_train_model.py     # Test functions for train_model.py
```