import hydra
import pandas as pd
from feature_engine.wrappers import SklearnTransformerWrapper
from hydra.utils import to_absolute_path
from omegaconf import DictConfig
from prefect import Flow, task
from prefect.engine.results import LocalResult
from prefect.engine.serializers import PandasSerializer
from sklearn.preprocessing import StandardScaler


@task
def load_data(data_name: str, load_kwargs: DictConfig) -> pd.DataFrame:
    return pd.read_csv(data_name, **load_kwargs)


@task
def drop_na(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()


def get_age(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(age=df["Year_Birth"].apply(lambda row: 2021 - row))


def get_total_children(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(total_children=df["Kidhome"] + df["Teenhome"])


def get_total_purchases(df: pd.DataFrame) -> pd.DataFrame:
    purchases_columns = df.filter(like="Purchases", axis=1).columns
    return df.assign(total_purchases=df[purchases_columns].sum(axis=1))


def get_enrollment_years(df: pd.DataFrame) -> pd.DataFrame:
    df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"])
    return df.assign(enrollment_years=2022 - df["Dt_Customer"].dt.year)


def get_family_size(df: pd.DataFrame, size_map: dict) -> pd.DataFrame:
    return df.assign(
        family_size=df["Marital_Status"].map(size_map) + df["total_children"]
    )


@task
def get_new_features(df: pd.DataFrame, size_map: dict) -> pd.DataFrame:
    return (
        df.pipe(get_age)
        .pipe(get_total_children)
        .pipe(get_total_purchases)
        .pipe(get_enrollment_years)
        .pipe(get_family_size, size_map=size_map)
    )


def drop_features(df: pd.DataFrame, drop_columns: list):
    return df.drop(drop_columns, axis=1).reset_index(drop=True)


def drop_outliers(df: pd.DataFrame, column_threshold: dict):
    for col, threshold in column_threshold.items():
        df = df[df[col] < threshold]
    return df


@task
def drop_columns_and_rows(df: pd.DataFrame, columns: DictConfig):
    return df.pipe(drop_features, drop_columns=columns["drop"]).pipe(
        drop_outliers, column_threshold=columns["remove_outliers_threshold"]
    )


@task
def scale_features(df: pd.DataFrame):
    scaler = SklearnTransformerWrapper(transformer=StandardScaler())
    return scaler.fit_transform(df)


@hydra.main(config_path="../config", config_name="process")
def process_data(config):
    with Flow(
        "process_data",
        result=LocalResult(
            to_absolute_path(config.intermediate.dir),
            location=config.intermediate.name,
            serializer=PandasSerializer("csv"),
        ),
    ) as flow:
        df = load_data(
            to_absolute_path(config.raw_data.path),
            config.raw_data.load_kwargs,
        )
        df = drop_na(df)
        df = get_new_features(df, config.encode.family_size)
        df = drop_columns_and_rows(df, config.columns)
        df = scale_features(df)

    return flow.run()


if __name__ == "__main__":
    process_data()
