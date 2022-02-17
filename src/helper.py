from functools import partial, wraps

import hydra
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from prefect import task
from prefect.backend.artifacts import create_markdown_artifact

import wandb


def artifact_task(func=None, **task_init_kwargs):

    if func is None:
        return partial(artifact_task, **task_init_kwargs)

    @wraps(func)
    def safe_func(**kwargs):
        res = func(**kwargs)
        if isinstance(res, pd.DataFrame):
            create_markdown_artifact(res.head(10).to_markdown())
        return res

    return task(safe_func, **task_init_kwargs)


@hydra.main(
    config_path="../config",
    config_name="main",
)
def initialize_wandb(config: DictConfig):
    wandb.init(
        project="customer_segmentation",
        config=OmegaConf.to_object(config),
        reinit=True,
        mode="disabled",
    )
