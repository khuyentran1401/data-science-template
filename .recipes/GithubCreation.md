# Create a Github repo

You can automate the creation and configuration of Github repositories using the [github CLI](https://github.com/cli/cli).

## Pre-requisites

One-time setup:
-   **Install**
    -   Mac: `brew install gh`
    -   Linux: [see instructions](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)
-   **Configure** - `gh auth login` and answer prompts as below:
    -   _What account do you want to log into?_ **Github.com**
    -   _What is your preferred protocol for Git operations?_ **SSH**
    -   _Upload your SSH public key to your Github account?_ Select the key you used to sign-up for 2-factor authentication with github
    -   _How would you like to authenticate GitHub CLI?_ **Login with a web browser**

## Recipe

```bash
source .cookiecutter/config # Get $REPO_NAME, $PROJECT_OPENNESS, and $DESCRIPTION based on the cookiecutter configuration

export GITHUB_ACCOUNT=<GITHUB ACCOUNT TO CREATE REPO IN>

# Create the Github repo
gh repo create "$GITHUB_ACCOUNT/$REPO_NAME" --"$PROJECT_OPENNESS" -d "$DESCRIPTION" -y 

# Configure the repo
gh api -X PATCH \
-F allow_merge_commit=false \
-F allow_rebase_merge=false \
"repos/$GITHUB_ACCOUNT/$REPO_NAME"

# If `gh` is older than 2.3.0 then the `gh repo create` command already does this
git remote add origin "git@github.com:$GITHUB_ACCOUNT/$REPO_NAME"

git push --all
```
