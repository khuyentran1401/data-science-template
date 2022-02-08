import os
import wandb
from prefect import task
from functools import wraps, partial
from prefect.backend.artifacts import create_markdown_artifact
import pandas as pd  
from omegaconf import DictConfig, OmegaConf

def artifact_task(func=None, **task_init_kwargs):
  
    if func is None: 
        return partial(artifact_task, **task_init_kwargs)

    @wraps(func)
    def safe_func(**kwargs):
        res = func(**kwargs)
        if isinstance(res, pd.DataFrame):
            create_markdown_artifact(res.head(10).to_markdown())
        return res

    safe_func.__name__ = func.__name__
    
    return task(safe_func, **task_init_kwargs)

def log_data(data_name: str, type: str, dir: str = None) -> None:
    if dir is None:
        dir, file = os.path.split(data_name)
    else:
        file = data_name

    logged_data = wandb.Artifact(file, type=type)
    logged_data.add_dir(dir)
    wandb.log_artifact(logged_data)
