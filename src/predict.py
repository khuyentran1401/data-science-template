import bentoml
import pandas as pd  

df = pd.read_csv('data/final/reduce_dimension.csv')
sample = df.iloc[0:1, :]

service_name = "customer_segmentation_kmeans"
model_version = f"{service_name}:latest"

classifier = bentoml.sklearn.load_runner(model_version)
out = classifier.run(sample)
print(out)