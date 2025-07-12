import requests
import json

url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
params = {
    "app_id": "2468334f",
    "app_key": "30cac15e7cdfa5ba0e4d5ef0b26ae978",
    "results_per_page": 10,
    "what": "software developer",
    "max_days_old": 7
}

response = requests.get(url, params=params)

data = response.json()
with open("adzuna_response.json", "w") as f:
    json.dump(data, f, indent=4)
