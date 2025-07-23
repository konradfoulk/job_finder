from dotenv import load_dotenv
import os
import requests
from utils import output_to_csv

load_dotenv()  # load environment variables to use os.environ


def find_jobs(query: str, ai_remote: str = None, ai_experience: str = None, limit: int = 10, file_name: str = 'jobs'):
    url = "https://active-jobs-db.p.rapidapi.com/active-ats-7d"  # api url

    # define api parameters for api request
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
        "x-rapidapi-key": os.environ['fantastic_x-rapidapi-key'],
        "x-rapidapi-host": "active-jobs-db.p.rapidapi.com"
    }

    # get data from api
    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    # format data into workable format
    jobs = []
    for i in data:
        job = {}

        job['id'] = i['id']
        job['title'] = i.get('title')
        job['company'] = i.get('organization')
        job['url'] = i.get('url')
        jobs.append(job)

    # output formated data to a csv
    output_to_csv(file_name, jobs)
