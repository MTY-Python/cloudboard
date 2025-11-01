import requests
import json

data = {
    "notes": [
        {"author": "Yusuf", "color": "yellow", "text": "Ferrari"},
        {"author": "Tom", "color": "brown", "text": "Hilton"},
        {"author": "Monty", "color": "black", "text": "Marriot"}
    ]
}

response = requests.post("http://localhost:5000/organise", json=data)
print(json.dumps(response.json(), indent=4))