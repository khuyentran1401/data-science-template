import bentoml
import bentoml.sklearn
import numpy as np
from bentoml.io import PandasDataFrame, NumpyNdarray

service_name = "customer_segmentation_kmeans"
model_version = f"customer_segmentation_kmeans:latest"

classifier = bentoml.sklearn.load_runner(model_version)
service = bentoml.Service(service_name, runners=[classifier])


@service.api(input=PandasDataFrame(), output=NumpyNdarray())
def predict(input_dataframe: PandasDataFrame) -> np.ndarray:
    result = classifier.run(input_dataframe)
    return result
