"""
Print the hydra configuration file
"""

import hydra
from omegaconf import DictConfig, OmegaConf

@hydra.main(version_base=None, config_path="./", config_name="main")
def print_hydra(config: DictConfig) -> None:
    print(OmegaConf.to_yaml(config))

if __name__ == "__main__":
    print_hydra()
