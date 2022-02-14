import json
import math

import requests
import streamlit as st

st.title("Customer Segmentation Web App")

data = {}

data["Income"] = st.number_input(
    "Income",
    min_value=0,
    step=500,
    value=58138,
    help="Customer's yearly household income",
)
data["Recency"] = st.number_input(
    "Recency",
    min_value=0,
    value=58,
    help="Number of days since customer's last purchase",
)
data["NumWebVisitsMonth"] = st.number_input(
    "NumWebVisitsMonth",
    min_value=0,
    value=7,
    help="Number of visits to company’s website in the last month",
)
data["Complain"] = st.number_input(
    "Complain",
    min_value=0,
    value=7,
    help="1 if the customer complained in the last 2 years, 0 otherwise",
)
data["age"] = st.number_input(
    "age",
    min_value=0,
    value=64,
    help="Customer's age",
)
data["total_purchases"] = st.number_input(
    "total_purchases",
    min_value=0,
    value=25,
    help="Total number of purchases through website, catalogue, or store",
)
data["enrollment_years"] = st.number_input(
    "enrollment_years",
    min_value=0,
    value=10,
    help="Number of years a client has enrolled with a company",
)
data["family_size"] = st.number_input(
    "family_size",
    min_value=0,
    value=1,
    help="Total number of members in a customer's family",
)


if st.button("Get the cluster of this customer"):
    if not any(math.isnan(v) for v in data.values()):
        data_json = json.dumps(data)

        prediction = requests.post(
            "http://127.0.0.1:5000/predict",
            headers={"content-type": "application/json"},
            data=data_json,
        ).text
        st.write(f"This customer belongs to the cluster {prediction}")
