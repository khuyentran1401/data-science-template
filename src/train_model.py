"""Python script to train the model"""
import joblib
import numpy as np
import pandas as pd
from config import Location, ModelParams
from prefect import flow, task
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC


@task
def get_processed_data(data_location: str):
    """Get processed data from a specified location

    Parameters
    ----------
    data_location : str
        Location to get the data
    """
    return joblib.load(data_location)


@task
def train_model(
    model_params: ModelParams, X_train: pd.DataFrame, y_train: pd.Series
):
    """Train the model

    Parameters
    ----------
    model_params : ModelParams
        Parameters for the model
    X_train : pd.DataFrame
        Features for training
    y_train : pd.Series
        Label for training
    """
    grid = GridSearchCV(SVC(), model_params.dict(), refit=True, verbose=3)
    grid.fit(X_train, y_train)
    return grid


@task
def predict(grid: GridSearchCV, X_test: pd.DataFrame):
    """_summary_

    Parameters
    ----------
    grid : GridSearchCV
    X_test : pd.DataFrame
        Features for testing
    """
    return grid.predict(X_test)


@task
def save_model(model: GridSearchCV, save_path: str):
    """Save model to a specified location

    Parameters
    ----------
    model : GridSearchCV
    save_path : str
    """
    joblib.dump(model, save_path)


@task
def save_predictions(predictions: np.array, save_path: str):
    """Save predictions to a specified location

    Parameters
    ----------
    predictions : np.array
    save_path : str
    """
    joblib.dump(predictions, save_path)


@flow
def train(
    location: Location = Location(),
    svc_params: ModelParams = ModelParams(),
):
    """Flow to train the model

    Parameters
    ----------
    location : Location, optional
        Locations of inputs and outputs, by default Location()
    svc_params : ModelParams, optional
        Configurations for training the model, by default ModelParams()
    """
    data = get_processed_data(location.data_process)
    model = train_model(svc_params, data["X_train"], data["y_train"])
    predictions = predict(model, data["X_test"])
    save_model(model, save_path=location.model)
    save_predictions(predictions, save_path=location.data_final)


if __name__ == "__main__":
    train()
