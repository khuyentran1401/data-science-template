[![View article](https://img.shields.io/badge/Data_Science_Simplified-View_article-blue)](https://mathdatasimplified.com/2023/06/17/how-to-structure-a-data-science-project-for-readability-and-transparency-2/) [![View on YouTube](https://img.shields.io/badge/YouTube-Watch%20on%20Youtube-red?logo=youtube)](https://youtu.be/TzvcPi3nsdw) 

# Directory structure template for Data Science projects

## Why?
It is important to structure your data science project based on a certain standard so that your teammates can easily maintain and modify your project.

This repository provides a template that incorporates best practices to create a maintainable and reproducible data science project.

## How are the templates organized?

The templates are organized in different branches, where each template is expected to be used along with a pre-determined set of tools. Depending on your approach (e.g., whether you want to use a cloud-based or on-premise ML project), you might want to use one template over others. In any case, the directory structure should not vary drastically.

## About this approach

The `aws-sagemaker` branch provides to you a directory structure to work with the Amazon SageMaker, an end-to-end cloud-based ML service offered by Amazon Web Sercevies (AWS). The following tools are expected to be used:

| Package management | Config file manager | Data version control |
|   ---               |        ---          |     ---              |
|   [Poetry](https://mathdatasimplified.com/poetry-a-better-way-to-manage-python-dependencies)        |       [Hydra](https://mathdatasimplified.com/stop-hard-coding-in-a-data-science-project-use-configuration-files-instead/)         |   [Amazon S3](https://aws.amazon.com/s3/)          |

* [pre-commit plugins](https://pre-commit.com/): Automate code reviewing formatting
* [pdoc](https://github.com/pdoc3/pdoc): Automatically create an API documentation for your project

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
│   ├── raw                         # raw data
│   └── raw.dvc                     # DVC file of data/raw
├── docs                            # documentation for your project
├── .gitignore                      # ignore files that cannot commit to Git
├── Makefile                        # store useful commands to set up the environment
├── models                          # store models
├── notebooks                       # store notebooks
├── .pre-commit-config.yaml         # configurations for pre-commit
├── pyproject.toml                  # dependencies for poetry
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

## How to use this project

1. Install Cookiecutter:
    ```bash
    pip install cookiecutter
    ```
1. Create a project based on the template:
    ```bash
    cookiecutter https://github.com/khuyentran1401/data-science-template --checkout aws-sagemaker
    ```

