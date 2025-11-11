import requests

url = "http://127.0.0.1:5000/rewrite"
data = {
    "email": "Hi team, I need the report asap. Thanks.",
    "tone": "formal"
}

response = requests.post(url, json=data)
print(response.json())