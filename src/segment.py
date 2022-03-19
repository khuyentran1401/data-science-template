from datetime import timedelta
from typing import Tuple

import hydra
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from prefect import Flow, case, task
from prefect.engine.results import LocalResult
from prefect.engine.serializers import PandasSerializer
from prefect.tasks.control_flow import merge
from sklearn.cluster import (DBSCAN, OPTICS, AffinityPropagation,
                             AgglomerativeClustering, Birch, KMeans, MeanShift,
                             SpectralClustering)
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from yellowbrick.cluster import KElbowVisualizer

import wandb

FINAL_OUTPUT = LocalResult(
    "data/final/",
    location="{task_name}.csv",
    serializer=PandasSerializer("csv", serialize_kwargs={"index": False}),
)


@task
def initialize_wandb(config: DictConfig):
    wandb.init(
        project="customer_segmentation",
        config=OmegaConf.to_object(config),
        reinit=True,
        mode=config.wandb_mode,
    )


@task
def get_pca_model(data: pd.DataFrame) -> PCA:

    pca = PCA(n_components=3)
    pca.fit(data)
    return pca


@task
def reduce_dimension(df: pd.DataFrame, pca: PCA) -> pd.DataFrame:
    return pd.DataFrame(pca.transform(df), columns=["col1", "col2", "col3"])


@task
def get_3d_projection(pca_df: pd.DataFrame) -> dict:
    """A 3D Projection Of Data In The Reduced Dimensionality Space"""
    return {"x": pca_df["col1"], "y": pca_df["col2"], "z": pca_df["col3"]}


@task
def check_has_nclusters(config: DictConfig):
    args = config.segment.args
    return args is not None and "n_clusters" in args


@task
def get_best_k_cluster(
    pca_df: pd.DataFrame, image_path: str, elbow_metric: str
) -> pd.DataFrame:

    fig = plt.figure(figsize=(10, 8))
    fig.add_subplot(111)

    elbow = KElbowVisualizer(KMeans(), metric=elbow_metric)
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


@task
def predict_with_predefined_clusters(
    pca_df: pd.DataFrame, k: int, model: dict
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Get model with the parameter `n_clusters`"""

    model_args = dict(model.args)
    model_args["n_clusters"] = k

    model = eval(model.algorithm)(**model_args)

    # Predict
    return model.fit_predict(pca_df)


@task
def predict_without_predefined_clusters(
    pca_df: pd.DataFrame, model: dict
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Get model without the parameter `n_clusters`"""
    if model.args is None:
        model_args = {}
    else:
        model_args = dict(model.args)
    model = eval(model.algorithm)(**model_args)

    # Predict
    return model.fit_predict(pca_df)


@task
def get_silhouette_score(pca_df: pd.DataFrame, labels: pd.DataFrame) -> float:
    sil_score = silhouette_score(pca_df, labels)
    wandb.log({"silhouette_score": sil_score})
    return sil_score


@task
def plot_silhouette_score(
    pca_df: pd.DataFrame, silhouette_score: float, image_path: str
):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111)

    ax.set_xlim([-1, 1])
    ax.set_ylim([0, len()])
    plt.plot(silhouette_score)
    plt.savefig(image_path)
    wandb.log({"silhouette_score_plot": wandb.Image(image_path)})


@task(result=FINAL_OUTPUT)
def insert_clusters_to_df(df: pd.DataFrame, clusters: np.ndarray) -> pd.DataFrame:
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


@task
def wandb_log(config: DictConfig):

    # log data
    wandb.log_artifact(config.raw_data.path, name="raw_data", type="data")
    wandb.log_artifact(config.intermediate.path, name="intermediate_data", type="data")
    wandb.log_artifact(config.segmented.path, name="segmented_data", type="data")

    # log number of columns
    wandb.log({"num_cols": len(config.process.keep_columns)})


@hydra.main(config_path="../config", config_name="main")
def segment(config: DictConfig) -> None:

    with Flow("segmentation") as flow:

        initialize_wandb(config)

        data = pd.read_csv(config.intermediate.path)
        pca = get_pca_model(data)
        pca_df = reduce_dimension(data, pca)

        projections = get_3d_projection(pca_df)

        has_nclusters = check_has_nclusters(config)

        with case(has_nclusters, True):
            k_best = get_best_k_cluster(pca_df, config.image.elbow, config.elbow_metric)
            prediction1 = predict_with_predefined_clusters(
                pca_df, k_best, config.segment
            )

        with case(has_nclusters, False):
            prediction2 = predict_without_predefined_clusters(pca_df, config.segment)

        prediction = merge(prediction1, prediction2)

        score = get_silhouette_score(pca_df, prediction)

        data = insert_clusters_to_df(data, prediction)

        plot_clusters(pca_df, prediction, projections, config.image.clusters)

        wandb_log(config)

    flow.run()
    # flow.visualize()
    # flow.register(project_name="customer_segmentation")


if __name__ == "__main__":
    segment()
