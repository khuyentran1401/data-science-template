from jinja2.ext import Extension

def _get_pkg_dependency_filename(v) -> str:
    out = {
        "pip": "requirements.txt",
        "poetry": "pyproject.toml"
    }
    return out[v]

class Jinja2Extension(Extension):
    """
    Adds new filters to the Jinja2 environment in which CookieCutter runs.
    """
    def __init__(self, environment):
        super(Jinja2Extension, self).__init__(environment)
        environment.filters['dep_filename'] = _get_pkg_dependency_filename