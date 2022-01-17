import hydra
import pandas as pd
from hydra.utils import to_absolute_path
from omegaconf import DictConfig
from prefect import Flow, task


@task
def load_data(data_name: str, load_kwargs: DictConfig) -> pd.DataFrame:
    return pd.read_csv(data_name, **load_kwargs)


@task
def drop_na(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()


@task
def get_age(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(age=df["Year_Birth"].apply(lambda row: 2021 - row))


@hydra.main(config_path="../config", config_name="load_data")
def process_data(config):
    with Flow("process_data") as flow:
        df = load_data(
            to_absolute_path(config.raw_data.path), config.raw_data.load_kwargs
        )
        df = drop_na(df)
        df = get_age(df)

    return flow.run()


if __name__ == "__main__":
    process_data()
