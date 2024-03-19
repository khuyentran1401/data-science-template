"""
This is the demo code that uses hydra to access the parameters in under the directory config.

Author: Khuyen Tran
"""

import hydra
from omegaconf import DictConfig


@hydra.main(config_path="../config", config_name="main", version_base="1.2")
def train_model(config: DictConfig):
    """Function to train the model"""

    print(f"Train modeling using {config.data.processed}")
    print(f"Model used: {config.model.name}")
    print(f"Save the output to {config.data.final}")


if __name__ == "__main__":
    train_model()
