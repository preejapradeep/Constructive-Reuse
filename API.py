import requests
import json

url = "https://api-dev.isee4xai.com/api/trees/cbr_retrieve"

payload = json.dumps({
  "treeId": "649ad54b123d1ba6e8e1a802",
  "usecaseId": "64628149ae10f5340983902d",
  "topk": 5
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)