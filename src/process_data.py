from datetime import timedelta

import hydra
import pandas as pd
import wandb
from omegaconf import DictConfig
from prefect import Flow, Parameter, task
from prefect.engine.results import LocalResult
from prefect.engine.serializers import PandasSerializer
from sklearn.preprocessing import StandardScaler

INTERMEDIATE_OUTPUT = LocalResult(
    "data/intermediate/",
    location="{task_name}.csv",
    serializer=PandasSerializer("csv", serialize_kwargs={"index": False}),
)


@task
def load_data(data_name: str) -> pd.DataFrame:
    data = pd.read_csv(data_name)
    return data


@task
def drop_na(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()


@task
def get_age(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(age=df["Year_Birth"].apply(lambda row: 2021 - row))


@task
def get_total_children(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(total_children=df["Kidhome"] + df["Teenhome"])


@task
def get_total_purchases(df: pd.DataFrame) -> pd.DataFrame:
    purchases_columns = df.filter(like="Purchases", axis=1).columns
    return df.assign(total_purchases=df[purchases_columns].sum(axis=1))


@task
def get_enrollment_years(df: pd.DataFrame) -> pd.DataFrame:
    df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"])
    return df.assign(enrollment_years=2022 - df["Dt_Customer"].dt.year)


@task
def get_family_size(df: pd.DataFrame, size_map: dict) -> pd.DataFrame:
    return df.assign(
        family_size=df["Marital_Status"].map(size_map) + df["total_children"]
    )


def drop_features(df: pd.DataFrame, keep_columns: list):
    df = df[keep_columns]
    return df


def drop_outliers(df: pd.DataFrame, column_threshold: dict):
    for col, threshold in column_threshold.items():
        df = df[df[col] < threshold]
    return df.reset_index(drop=True)


@task(result=INTERMEDIATE_OUTPUT)
def drop_columns_and_rows(df: pd.DataFrame, columns: DictConfig) -> pd.DataFrame:
    df = df.pipe(drop_features, keep_columns=columns.keep).pipe(
        drop_outliers, column_threshold=columns.remove_outliers_threshold
    )

    return df


@task(result=LocalResult("processors", location="scaler.pkl"))
def get_scaler(df: pd.DataFrame):
    scaler = StandardScaler()
    scaler.fit(df)

    return scaler


@task(result=INTERMEDIATE_OUTPUT)
def scale_features(df: pd.DataFrame, scaler: StandardScaler):
    return pd.DataFrame(scaler.transform(df), columns=df.columns)


@hydra.main(
    config_path="../config",
    config_name="main",
)
def process_data(config: DictConfig):

    with Flow("process_data") as flow:
        df = load_data(config.raw_data.path)
        df = drop_na(df)
        df = get_age(df)
        df = get_total_children(df)
        df = get_total_purchases(df)
        df = get_enrollment_years(df)
        df = get_family_size(df, config.process.encode.family_size)
        df = drop_columns_and_rows(df, config.process.columns)
        scaler = get_scaler(df)
        df = scale_features(df, scaler)

    flow.run()
    # flow.register(project_name="customer_segmentation")


if __name__ == "__main__":
    process_data()
