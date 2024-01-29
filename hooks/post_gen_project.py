import os


if __name__ == "__main__":
    if "{{ cookiecutter.data_version_control }}" == "yes":
        # create .dvc/ directory
        if not os.path.exists(".dvc"):
            os.mkdir(".dvc")
        # create .dvc/.gitignore
        gitignore_content = "/config.local\n/tmp\n/cache"
        with open(os.path.join(".dvc", ".gitignore"), 'w') as file:
            file.write(gitignore_content)
        # create .dvc/config
        with open(os.path.join(".dvc", "config"), 'w') as _:
            pass