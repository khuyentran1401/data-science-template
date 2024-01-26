from jinja2.ext import Extension
import requests


def _is_404(v) -> bool:
    response = requests.get(v)
    return response.status_code == 404

class GithubExtension(Extension):
    def __init__(self, environment):
        super(GithubExtension, self).__init__(environment)
        environment.filters['is_404'] = lambda v: _is_404(v)
