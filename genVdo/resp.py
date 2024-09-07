import requests

url = "http://127.0.0.1:5000/clean"
data = {"text": "Hello, World! 🌍 ** ####This is a test! #Python123^2 😄✨"}
response = requests.post(url, json=data)

print(response.json())
