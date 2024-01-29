import os

def parse_dvc_settings():
    if "{{ cookiecutter.data_version_control }}" == "no":
        os.rmdir(".dvc")
        os.remove(os.path.join(".dvc", ".gitignore"))
        os.remove(os.path.join(".dvc", "config"))
        os.remove(os.path.join("data", "raw.dvc"))
        os.remove("dvc.yaml")

if __name__ == "__main__":
    parse_dvc_settings()