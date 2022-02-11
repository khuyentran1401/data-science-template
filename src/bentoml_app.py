import bentoml
import bentoml.sklearn
import numpy as np
import pandas as pd 
from bentoml.io import PandasDataFrame, NumpyNdarray, Text
import pickle 

service_name = "customer_segmentation_kmeans"
model_version = f"customer_segmentation_kmeans:latest"

classifier = bentoml.sklearn.load_runner(model_version)
service = bentoml.Service(service_name, runners=[classifier])


@service.api(input=Text(), output=NumpyNdarray())
def predict(data_name: Text) -> np.ndarray:

    # Read data
    input_sample = pd.read_csv(data_name)
    
    # Process data
    pca = pickle.load(open("../model/PCA.pkl", "rb"))
    processed = pd.DataFrame(pca.transform(input_sample), columns=['col1', 'col2', 'col3'])

    # Predict
    result = classifier.run(processed)
    return np.array(result)
