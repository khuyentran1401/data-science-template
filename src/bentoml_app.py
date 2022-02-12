import pickle

import bentoml
import bentoml.sklearn
import numpy as np
import pandas as pd
from bentoml.io import JSON, NumpyNdarray
from pydantic import BaseModel

service_name = "customer_segmentation_kmeans"
model_version = f"{service_name}:latest"

classifier = bentoml.sklearn.load_runner(model_version)
service = bentoml.Service(service_name, runners=[classifier])


class Customer(BaseModel):

    Income: int = 58138
    Recency: int = 58
    MntWines: int = 635
    MntFruits: int = 88
    MntMeatProducts: int = 546
    MntFishProducts: int = 172
    MntSweetProducts: int = 88
    MntGoldProds: int = 88
    Complain: int = 0
    Response: int = 1
    age: int = 64
    enrollment_years: int = 64
    family_size: int = 1


@service.api(input=JSON(pydantic_model=Customer), output=NumpyNdarray())
def predict(customer: JSON(pydantic_model=Customer)) -> np.ndarray:

    df = pd.DataFrame(customer.dict(), index=[0])

    # Process data
    scaler = pickle.load(open("../model/scaler.pkl", "rb"))
    scaled_df = scaler.transform(df)

    pca = pickle.load(open("../model/PCA.pkl", "rb"))
    processed = pd.DataFrame(
        pca.transform(scaled_df), columns=["col1", "col2", "col3"]
    )

    # Predict
    result = classifier.run(processed)
    return np.array(result)
