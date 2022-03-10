import hydra
import wandb
from omegaconf import DictConfig, OmegaConf

from process_data import process_data
from segment import segment


@hydra.main(
    config_path="../config",
    config_name="main",
)
def main(config: DictConfig):

    process_data(config)
    segment(config)


if __name__ == "__main__":
    main()
