import os

import wandb


def log_data(data_name: str, type: str, dir: str = None) -> None:
    if dir is None:
        dir, file = os.path.split(data_name)
    else:
        file = data_name

    logged_data = wandb.Artifact(file, type=type)
    logged_data.add_dir(dir)
    wandb.log_artifact(logged_data)
