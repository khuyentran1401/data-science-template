import hydra
from omegaconf import DictConfig, OmegaConf

import wandb
from process_data import process_data
from segment import segment


@hydra.main(
    config_path="../config",
    config_name="main",
)
def main(config: DictConfig):

    wandb.init(
        project="customer_segmentation",
        config=OmegaConf.to_object(config),
        reinit=True,
        mode="disabled",
    )

    if config.flow == "all":
        process_data(config)
        segment(config)

    elif config.flow == "process_data":
        process_data(config)

    elif config.flow == "segment":
        segment(config)

    else:
        print("flow not found")


if __name__ == "__main__":
    main()
