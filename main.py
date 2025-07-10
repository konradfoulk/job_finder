import requests

url = "https://active-jobs-db.p.rapidapi.com/active-ats-1h"

querystring = {"offset": "0", "advanced_title_filter": "(developer | 'software engineer' | (engineer & ('full stack' | frontend | backend))) & (junior | jr | 'entry level') & ! senior", "location_filter": "\"United States\"",
               "description_filter": "python | javascript | JS | HTML | CSS", "description_type": "text", "include_ai": "true", "ai_work_arrangement_filter": "Remote OK,Remote Solely", "ai_experience_level_filter": "0-2,2-5", "include_li": "true"}

headers = {
    "x-rapidapi-key": "d36f4588c5msh61ad8b784cc92d0p1e1eadjsn79df372055f9",
    "x-rapidapi-host": "active-jobs-db.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
