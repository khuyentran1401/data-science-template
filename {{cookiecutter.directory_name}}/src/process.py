"""
This is the ETL procedure code that takes in data sources and returns backroom data.

Author: Pranav Arora
"""

import hydra
import pandas as pd
from omegaconf import DictConfig


@hydra.main(config_path="../config", config_name="main", version_base=None)
def process_data(config: DictConfig):
    """Function to process the data"""

    print(f"Process data using {config.data.raw}")
    print(f"Columns used: {config.process.use_columns}")

    data = pd.read_csv(config.data.raw)
    print(data.to_string())



if __name__ == "__main__":
    process_data()
