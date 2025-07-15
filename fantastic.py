import requests
from output_to_csv import output_to_csv


def find_jobs(query: str, ai_remote: str = None, ai_experience: str = None, limit: int = 10, name: str = 'jobs'):
    url = "https://active-jobs-db.p.rapidapi.com/active-ats-7d"

    querystring = {
        "limit": limit,
        "offset": "0",
        "advanced_title_filter": query,
        "location_filter": "\"United States\"",
        "description_type": "text"
    }

    if ai_remote and ai_experience:
        querystring.update({
            "ai_work_arrangement_filter": ai_remote,
            "ai_experience_level_filter": ai_experience
        })
    elif ai_remote:
        querystring["ai_work_arrangement_filter"] = ai_remote
    elif ai_experience:
        querystring["ai_experience_level_filter"] = ai_experience

    headers = {
        "x-rapidapi-key": "d36f4588c5msh61ad8b784cc92d0p1e1eadjsn79df372055f9",
        "x-rapidapi-host": "active-jobs-db.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    jobs = []
    for i in data:
        job = {}

        job['id'] = i['id']
        job['title'] = i.get('title')
        job['company'] = i.get('organization')
        job['url'] = i.get('url')
        jobs.append(job)

    output_to_csv(name, jobs)

# developer | 'software engineer' | (('full stack' | frontend | backend) & engineer)
