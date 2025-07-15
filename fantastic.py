import requests
import json

url = "https://active-jobs-db.p.rapidapi.com/active-ats-7d"

querystring = {
    "limit": "10",
    "offset": "0",
    "advanced_title_filter": "developer | 'software engineer' | (('full stack' | frontend | backend) & engineer)",
    "location_filter": "\"United States\"",
    "description_type": "text",
    "include_ai": "true",
    "ai_work_arrangement_filter": "Remote OK,Remote Solely",
    "ai_experience_level_filter": "0-2",
    "include_li": "true"
}

headers = {
    "x-rapidapi-key": "d36f4588c5msh61ad8b784cc92d0p1e1eadjsn79df372055f9",
    "x-rapidapi-host": "active-jobs-db.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

data = response.json()
with open("fantastic_response.json", "w") as f:
    json.dump(data, f, indent=4)
