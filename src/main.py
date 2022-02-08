import hydra
from omegaconf import DictConfig, OmegaConf

import wandb
from process_data import process_data
from segment import segment


@hydra.main(config_path="../config", config_name="main")
def main(config: DictConfig):
    wandb.init(
            project="customer_segmentation", config=OmegaConf.to_object(config)
        )

    if config.pipeline == 'all':
        process_data(config)
        segment(config)
    
    elif config.pipeline == 'process_data':
        process_data(config)
    
    elif config.pipeline == 'segment':
        segment(config)

    else: 
        print("Pipeline not found")


if __name__ == "__main__":
    main()
