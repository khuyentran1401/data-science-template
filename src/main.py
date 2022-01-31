import hydra
from omegaconf import DictConfig, OmegaConf
from prefect import Flow

import wandb
from process_data import process_data
from segment import segment


@hydra.main(config_path="../config", config_name="main")
def main(config: DictConfig):
    with Flow(
        "segmentation",
    ) as flow:
        wandb.init(
            project="customer_segmentation", config=OmegaConf.to_object(config)
        )
        process_data(config)
        segment(config)
    flow.run()


if __name__ == "__main__":
    main()
