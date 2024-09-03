import requests
import json

url = "https://modelslab.com/api/v6/video/open_sora"

payload = json.dumps({
     "key":"DoI5KTEzvxCGMKt4m4qDAkX8Dihzv5w1w8qQMadPfCDXCQqAofwxTeppIZAP",
    "prompt":"a dog playing cards",
    "height": 556,
    "width":556,
    "num_frames": 150,
    "fps":16,
    "webhook":None,
    "track_id": None
})

headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

