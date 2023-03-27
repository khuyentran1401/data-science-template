# Metaflow on AWS

To use Metaflow on AWS, you need.

-   Ensure:

    -   AWS CLI is installed and configured to use the Nesta datascience account

        <details>

        -   **Install** - `pip install awscli`

        -   **Configure**

            Fetch (or generate) security credentials from the AWS dashboard by clicking "Create access key".

            Run `aws configure`, inputting the access key ID and secret access key ID you just generated when prompted.

            In addition you should set the default region name to `eu-west-2` and the default output format to `json`.

            AWS provide a more detailed guide [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config).

        </details>

    -   You are part of the `DataScience` IAM group on AWS, requesting approval if not.

-   Add `metaflow` to `requirements.txt`
-   Fetch the Metaflow configuration `aws secretsmanager get-secret-value --secret-id dap-infra/metaflow/config --query SecretString --output text > "$HOME/.metaflowconfig/config_ds-cookiecutter.json"`
-   [Optional] Add `export METAFLOW_PROFILE=ds-cookiecutter` to your `.envrc` file to automatically activate this Metaflow profile within your project.
    -   If you do not add this to your `.envrc` file then you need to make sure the environment variable is set from where you run your Metaflows.
