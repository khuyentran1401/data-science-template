"""
Create an iris flow
"""
from config import Location, ModelParams, ProcessConfig
from prefect import flow
from process import process
from run_notebook import run_notebook
from train_model import train


@flow
def iris_flow(
    location: Location = Location(),
    process_config: ProcessConfig = ProcessConfig(),
    model_params: ModelParams = ModelParams(),
):
    """Flow to run the process, train, and run_notebook flows

    Parameters
    ----------
    location : Location, optional
        Locations of inputs and outputs, by default Location()
    process_config : ProcessConfig, optional
        Configurations for processing data, by default ProcessConfig()
    model_params : ModelParams, optional
        Configurations for training models, by default ModelParams()
    """
    process(location, process_config)
    train(location, model_params)
    run_notebook(location)


if __name__ == "__main__":
    iris_flow()
