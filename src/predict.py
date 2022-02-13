import requests

prediction = requests.post(
    "http://127.0.0.1:5000/predict",
    headers={"content-type": "application/json"},
    data='{"Income": 58138, "Recency": 58, "Complain": 0,"age": 64,"total_purchases": 25,"enrollment_years": 10,"family_size": 1}',
).text

print(prediction)
