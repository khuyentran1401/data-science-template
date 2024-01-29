import os

dvc_yaml_content = """stages:
  process_data:
    cmd: python src/process.py
    deps:
    - config/main.yaml
    - config/process
    - data/raw
    - src/process.py
    outs:
    - data/processed:
        persist: true
  train_model:
    cmd: python src/train_model.py
    deps:
    - config/main.yaml
    - config/model
    - data/processed
    - src/train_model.py
    outs:
    - data/final:
        persist: true
    - models:
        persist: true"""

gitignore_content = """/config.local
/tmp
/cache"""

data_raw_dvc_content = """outs:
- md5: 6ffbaaad7b4ac6e1afabed19a80b2560.dir
  size: 0
  nfiles: 1
  path: raw"""

def parse_dvc_settings():
    if "{{ cookiecutter.data_version_control }}" == "yes":
        # create .dvc/ directory
        if not os.path.exists(".dvc"):
            os.mkdir(".dvc")
        # create .dvc/.gitignore
        with open(os.path.join(".dvc", ".gitignore"), "w") as file:
            file.write(gitignore_content)
        # touch .dvc/config
        with open(os.path.join(".dvc", "config"), "w") as _:
            pass
        # create data/raw.dvc
        with open(os.path.join("data", "raw.dvc"), "w") as file:
            file.write(data_raw_dvc_content)
        # create dvc.yaml
        with open("dvc.yaml", "w") as file:
            file.write(dvc_yaml_content)

if __name__ == "__main__":
    parse_dvc_settings()