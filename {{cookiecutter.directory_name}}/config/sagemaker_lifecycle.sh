#!/bin/bash

# config git
git config --global user.email "{{ cookiecutter.github_email }}"
git config --global user.name "{{ cookiecutter.your_github_repo.split('/')[3] }}"
git config --global credential.helper cache
git config --global credential.helper "cache --timeout=86400"
# remove conda environment
sudo rm -rf /opt/conda ~/.conda
# install vanilla python interpreter
sudo apt install -y python3 python3-pip
# install poetry
pip install poetry
# add user ~/.local/bin to $PATH
sudo sed -i '$a export PATH="~/.local/bin${PATH:+:${PATH}}"' /etc/bash.bashrc
# clone the repo
git clone -C /home/sagemaker-user clone {{ cookiecutter.your_github_repo }}
