import bentoml
import pandas as pd
import pickle 

df = pd.read_csv("data/test/sample1.csv")
pca = pickle.load(open("model/PCA.pkl", "rb"))
processed = pd.DataFrame(pca.transform(df), columns=['col1', 'col2', 'col3'])

service_name = "customer_segmentation_kmeans"
model_version = f"{service_name}:latest"

classifier = bentoml.sklearn.load_runner(model_version)
out = classifier.run(processed)
print(out)
