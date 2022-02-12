import pickle

import bentoml
import pandas as pd

# ---------------------------------------------------------------------------- #
# Load data
df = pd.read_csv("data/test/sample1.csv")

# ---------------------------------------------------------------------------- #
# Process data
scaler = pickle.load(open("model/scaler.pkl", "rb"))
scaled_df = scaler.transform(df)

pca = pickle.load(open("model/PCA.pkl", "rb"))
processed = pd.DataFrame(
    pca.transform(scaled_df), columns=["col1", "col2", "col3"]
)

# ---------------------------------------------------------------------------- #
# Predict
service_name = "customer_segmentation_kmeans"
model_version = f"{service_name}:latest"

classifier = bentoml.sklearn.load_runner(model_version)
out = classifier.run(processed)
print(out)
