import hydra

import wandb
from process_data import process_data
from segment import segment


@hydra.main(config_path="../config", config_name="main")
def main(config):
    wandb.init(project="customer_segmentation", config=config)
    process_data(config)
    segment(config)


if __name__ == "__main__":
    main()
