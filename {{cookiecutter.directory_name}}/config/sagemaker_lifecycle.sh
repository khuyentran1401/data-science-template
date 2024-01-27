#!/bin/bash

# Unix shell script to config the AWS SageMaker lifecycle
# Paste it as a new lifecycle script to config your Code Editor space

# config git
git config --global user.email "{{ cookiecutter.github_email }}"
git config --global user.name "{{ cookiecutter.__username }}"
git config --global credential.helper cache
git config --global credential.helper "cache --timeout=86400"
# install poetry
pip install poetry
# add user ~/.local/bin to $PATH
echo 'export PATH="/home/sagemaker-user/.local/bin${PATH:+:${PATH}}"' >> /home/sagemaker-user/.bashrc
# clone the repo
git -C /home/sagemaker-user clone {{ cookiecutter.your_github_repo }}
