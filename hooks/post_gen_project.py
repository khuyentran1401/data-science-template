import os

def parse_dependencies_settings():
    if "{{ cookiecutter.dependency_manager }}" != "pip":
        os.remove("requirements.txt")
        os.remove("requirements-dev.txt")

if __name__ == "__main__":
    parse_dependencies_settings()