from datetime import timedelta
from typing import Tuple

import bentoml
import bentoml.sklearn
import hydra
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from omegaconf import DictConfig, OmegaConf
from prefect import Flow, task
from prefect.backend.artifacts import create_markdown_artifact
from prefect.engine.results import LocalResult
from prefect.engine.serializers import PandasSerializer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from yellowbrick.cluster import KElbowVisualizer

import wandb
from helper import artifact_task

FINAL_OUTPUT = LocalResult(
    "data/final/",
    location="{task_name}.csv",
    serializer=PandasSerializer("csv", serialize_kwargs={"index": False}),
)


@task(result=LocalResult("processors", location="PCA.pkl"))
def get_pca_model(data: pd.DataFrame) -> PCA:
    create_markdown_artifact(data.columns)

    pca = PCA(n_components=3)
    pca.fit(data)
    return pca


@artifact_task(result=FINAL_OUTPUT)
def reduce_dimension(df: pd.DataFrame, pca: PCA) -> pd.DataFrame:
    return pd.DataFrame(pca.transform(df), columns=["col1", "col2", "col3"])


@task
def get_3d_projection(pca_df: pd.DataFrame) -> dict:
    """A 3D Projection Of Data In The Reduced Dimensionality Space"""
    return {"x": pca_df["col1"], "y": pca_df["col2"], "z": pca_df["col3"]}


@task
def get_best_k_cluster(pca_df: pd.DataFrame, image_path: str) -> pd.DataFrame:

    fig = plt.figure(figsize=(10, 8))
    fig.add_subplot(111)

    elbow = KElbowVisualizer(KMeans(), metric="distortion")

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
def get_clusters_model(
    pca_df: pd.DataFrame, k: int
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    model = KMeans(n_clusters=k)

    # Fit model
    return model.fit(pca_df)


@task
def save_model(model):
    bentoml.sklearn.save("customer_segmentation_kmeans", model)


@task
def predict(model, pca_df: pd.DataFrame):
    return model.predict(pca_df)


@artifact_task(result=FINAL_OUTPUT)
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


@hydra.main(
    config_path="../config",
    config_name="main",
)
def segment(config: DictConfig) -> None:

    with Flow("segmentation") as flow:

        data = pd.read_csv(config.intermediate.path)

        pca = get_pca_model(data)

        pca_df = reduce_dimension(data, pca)

        projections = get_3d_projection(pca_df)

        k_best = get_best_k_cluster(
            pca_df,
            config.image.kmeans,
        )

        model = get_clusters_model(pca_df, k_best)
        save_model(model)

        preds = predict(model, pca_df)

        data = insert_clusters_to_df(data, preds)

        plot_clusters(
            pca_df,
            preds,
            projections,
            config.image.clusters,
        )

    flow.run()
    # flow.register(project_name="customer_segmentation")


if __name__ == "__main__":
    segment()
