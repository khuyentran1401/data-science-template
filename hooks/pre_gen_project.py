def _print_warning():
    repo_name = "{{ cookiecutter.your_github_repo }}"
    print(f"""
    The repository {repo_name} returned 404,
    indicating that is either do not exist or is private. In the
    former case, you must create it first before using this
    template. In the latter case, you can delete git clone command
    in ./config/sagemaker_lifecycle.sh and manually clone your
    repository. Alternatively, you can add your Personal Acess
    Token (PAT) to this command to automatically clone your
    repository in the Code Editor. For example,

    git clone {repo_name[:8] + "000000000@" + repo_name[8:] }

    Where 000000000 is your PAT.
    """)

if __name__ == "__main__":
    __is_404 = "{{ cookiecutter.__is_404 }}"
    if __is_404:
        _print_warning()