import os


def parse_dependencies_settings():
    if "{{ cookiecutter.dependency_manager }}" != "pip":
        os.remove("requirements.txt")
        os.remove("requirements-dev.txt")


def handle_python_version_file():
    """Remove .python-version file if not using uv."""
    if "{{ cookiecutter.dependency_manager }}" != "uv":
        os.remove(".python-version")


if __name__ == "__main__":
    parse_dependencies_settings()
    handle_python_version_file()
