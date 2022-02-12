import bentoml
import bentoml.sklearn
import pandas as pd
from feature_engine.wrappers import SklearnTransformerWrapper
from hydra.utils import to_absolute_path
from omegaconf import DictConfig
from prefect import Flow, task
from prefect.engine.results import LocalResult
from prefect.engine.serializers import PandasSerializer
from sklearn.preprocessing import StandardScaler
from wandb import wandb

from helper import artifact_task, log_data


@artifact_task
def load_data(data_name: str) -> pd.DataFrame:
    data = pd.read_csv(data_name)

    log_data(data_name, "raw_data")

    return data


@artifact_task
def drop_na(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()


@artifact_task
def get_age(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(age=df["Year_Birth"].apply(lambda row: 2021 - row))


@artifact_task
def get_total_children(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(total_children=df["Kidhome"] + df["Teenhome"])


@artifact_task
def get_total_purchases(df: pd.DataFrame) -> pd.DataFrame:
    purchases_columns = df.filter(like="Purchases", axis=1).columns
    return df.assign(total_purchases=df[purchases_columns].sum(axis=1))


@artifact_task
def get_enrollment_years(df: pd.DataFrame) -> pd.DataFrame:
    df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"])
    return df.assign(enrollment_years=2022 - df["Dt_Customer"].dt.year)


@artifact_task
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


@artifact_task(
    result=LocalResult(
        "data/intermediate",
        location="{task_name}.csv",
        serializer=PandasSerializer("csv", serialize_kwargs={"index": False}),
    )
)
def drop_columns_and_rows(df: pd.DataFrame, columns: DictConfig):
    df = df.pipe(drop_features, keep_columns=columns["keep"]).pipe(
        drop_outliers, column_threshold=columns["remove_outliers_threshold"]
    )

    return df


@task(result=LocalResult("model", location="scaler.pkl"))
def get_scaler(df: pd.DataFrame):
    scaler = SklearnTransformerWrapper(transformer=StandardScaler())
    scaler.fit(df)

    return scaler


@artifact_task
def scale_features(df: pd.DataFrame, scaler: SklearnTransformerWrapper):
    return scaler.fit_transform(df)


def process_data(config: DictConfig):
    data_config = config.data_catalog
    code_config = config.process

    with Flow(
        "process_data",
        result=LocalResult(
            to_absolute_path(data_config.intermediate.dir),
            location=data_config.intermediate.name,
            serializer=PandasSerializer("csv"),
        ),
    ) as flow:
        df = load_data(
            to_absolute_path(data_config.raw_data.path),
        )
        df = drop_na(df)
        df = get_age(df)
        df = get_total_children(df)
        df = get_total_purchases(df)
        df = get_enrollment_years(df)
        df = get_family_size(df, code_config.encode.family_size)
        df = drop_columns_and_rows(df, code_config.columns)
        scaler = get_scaler(df)
        df = scale_features(df, scaler)

    flow.run()
    flow.register(project_name="customer_segmentation")

    log_data(
        data_config.intermediate.name,
        "preprocessed_data",
        to_absolute_path(data_config.intermediate.dir),
    )

    wandb.config.update({"num_cols": len(code_config.columns.keep)})
