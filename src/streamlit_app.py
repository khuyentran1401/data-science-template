from email.policy import default

import streamlit as st

st.title("Customer Segmentation Web App")

st.number_input(
    "Income",
    min_value=0,
    step=500,
    value=58138,
    help="Customer's yearly household income",
)
st.number_input(
    "Recency",
    min_value=0,
    value=58,
    help="Number of days since customer's last purchase",
)
st.number_input(
    "MntWines",
    min_value=0,
    value=635,
    help="Amount spent on wine in last 2 years",
)
