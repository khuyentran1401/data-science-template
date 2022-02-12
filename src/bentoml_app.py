import pickle

import bentoml
import bentoml.sklearn
import numpy as np
import pandas as pd
from bentoml.io import JSON, NumpyNdarray, PandasDataFrame, Text
from pydantic import BaseModel, Field

service_name = "customer_segmentation_kmeans"
model_version = f"{service_name}:latest"

classifier = bentoml.sklearn.load_runner(model_version)
service = bentoml.Service(service_name, runners=[classifier])


class Customer(BaseModel):

    Income: float = 0.29
    Recency: float = 0.31
    mntWines: float = Field(default=0.98, alias="Mnt Wines")
    mntFruits: float = Field(default=1.55, alias="Mnt Fruits")
    mntMeat: float = Field(default=1.69, alias="Mnt Meat Products")


@service.api(input=JSON(pydantic_model=Customer), output=NumpyNdarray())
def predict(customer: dict) -> np.ndarray:

    return customer
    # # Read data
    # input_sample = pd.read_csv(data_name)

    # # Process data
    # pca = pickle.load(open("../model/PCA.pkl", "rb"))
    # processed = pd.DataFrame(pca.transform(input_sample), columns=['col1', 'col2', 'col3'])

    # # Predict
    # result = classifier.run(processed)
    # return np.array(result)
