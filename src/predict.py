import requests

prediction = requests.post(
    "http://127.0.0.1:5000/predict",
    headers={"content-type": "application/json"},
    data='{"Income": 58138, "Recency": 58,"MntWines": 635,"MntFruits": 88,"MntMeatProducts": 546,"MntFishProducts": 172,"MntSweetProducts": 88,"MntGoldProds": 88,"Complain": 0,"Response": 1,"age": 64,"enrollment_years": 10,"family_size": 1}',
).text

print(prediction)
