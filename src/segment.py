from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from hydra.utils import to_absolute_path
from omegaconf import DictConfig
from prefect import Flow, task
from prefect.engine.results import LocalResult
from prefect.engine.serializers import PandasSerializer
from sklearn.cluster import (DBSCAN, OPTICS, AffinityPropagation,
                             AgglomerativeClustering, Birch, KMeans, MeanShift,
                             SpectralClustering)
from sklearn.decomposition import PCA
from yellowbrick.cluster import KElbowVisualizer

import wandb
from helper import log_data
from loguru import logger
from rich import inspect 

OUTPUT_DIR = "data/final/"
OUTPUT_FILE = "segmented.csv"


@task
def reduce_dimension(
    df: pd.DataFrame, n_components: int, columns: list
) -> pd.DataFrame:
    pca = PCA(n_components=n_components)
    return pd.DataFrame(pca.fit_transform(df), columns=columns)


@task
def get_3d_projection(pca_df: pd.DataFrame) -> dict:
    """A 3D Projection Of Data In The Reduced Dimensionality Space"""
    return {"x": pca_df["col1"], "y": pca_df["col2"], "z": pca_df["col3"]}


@task
def create_3d_plot(projection: dict, image_path: str) -> None:

    # To plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(
        projection["x"],
        projection["y"],
        projection["z"],
        cmap="Accent",
        marker="o",
    )
    ax.set_title("A 3D Projection Of Data In The Reduced Dimension")
    plt.savefig(image_path)

    # Log plot
    wandb.log({"pca": wandb.Image(image_path)})


@task
def get_best_k_cluster(
    pca_df: pd.DataFrame, cluster_config, image_path: str
) -> pd.DataFrame:

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    model = eval(cluster_config.algorithm)()
    elbow = KElbowVisualizer(
        model, metric=cluster_config.metric
    )

    elbow.fit(pca_df)
    elbow.fig.savefig(image_path)

    k_best = elbow.elbow_value_

    # Log
    wandb.log(
        {
            "elbow": wandb.Image(image_path),
            "k_best": k_best,
            "score_best": elbow.elbow_score_,
        }
    )
    return k_best


@task()
def get_clusters(
    pca_df: pd.DataFrame, algorithm: str, k: int
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    model = eval(algorithm)(n_clusters=k)

    # Fit model and predict clusters
    return model.fit_predict(pca_df)


@task(
    result=LocalResult(
        OUTPUT_DIR,
        location=OUTPUT_FILE,
        serializer=PandasSerializer("csv"),
    ),
)
def insert_clusters_to_df(
    df: pd.DataFrame, clusters: np.ndarray
) -> pd.DataFrame:
    return df.assign(clusters=clusters)


@task
def plot_clusters(
    pca_df: pd.DataFrame, preds: np.ndarray, projections: dict, image_path: str
) -> None:
    pca_df["clusters"] = preds

    plt.figure(figsize=(10, 8))
    ax = plt.subplot(111, projection="3d")
    ax.scatter(
        projections["x"],
        projections["y"],
        projections["z"],
        s=40,
        c=pca_df["clusters"],
        marker="o",
        cmap="Accent",
    )
    ax.set_title("The Plot Of The Clusters")

    plt.savefig(image_path)

    # Log plot
    wandb.log({"clusters": wandb.Image(image_path)})


def segment(config: DictConfig) -> None:

    data_config = config.data_catalog
    code_config = config.segment

    with Flow(
        "segmentation",
    ) as flow:

        data = (
            LocalResult(
                dir=to_absolute_path(data_config.intermediate.dir),
                serializer=PandasSerializer(
                    "csv",
                    deserialize_kwargs=data_config.intermediate.deserialize_kwargs,
                ),
            )
            .read(location=data_config.intermediate.name)
            .value
        )

        pca_df = reduce_dimension(
            data, code_config.pca.n_components, code_config.pca.columns
        )

        projections = get_3d_projection(pca_df)

        create_3d_plot(projections, to_absolute_path(code_config.image.pca))

        k_best = get_best_k_cluster(
            pca_df,
            code_config.cluster,
            to_absolute_path(code_config.image.kmeans),
        )

        preds = get_clusters(pca_df, code_config.cluster.algorithm, k_best)

        data = insert_clusters_to_df(data, preds)

        plot_clusters(
            pca_df,
            preds,
            projections,
            to_absolute_path(code_config.image.clusters),
        )

    flow.run()
    # flow.visualize()
    log_data(
        data_config.segmented.name,
        "preprocessed_data",
        to_absolute_path(data_config.segmented.dir),
    )
