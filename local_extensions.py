from jinja2.ext import Extension

def get_pkg_dependency_filename(v) -> str:
    if v == "pip":
        return "requirements.txt"
    elif v == "poetry":
        return "pyproject.toml"

class GithubExtension(Extension):
    def __init__(self, environment):
        super(GithubExtension, self).__init__(environment)
        environment.filters['dep_filename'] = lambda v: get_pkg_dependency_filename(v)