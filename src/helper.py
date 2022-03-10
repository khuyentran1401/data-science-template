import hydra
import pandas as pd
import wandb
from omegaconf import DictConfig, OmegaConf


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
