from dotenv import load_dotenv
import os
import requests

load_dotenv()


def update_params(query, query_not, age):
    params = {
        "app_id": f"{os.environ['adzuna_app_id']}",
        "app_key": f"{os.environ['adzuna_app_key']}",
        "results_per_page": 50,
        'what': query,
        'max_days_old': age
    }

    if query_not:
        params['what_exclude'] = query_not

    return params


def get_jobs(params, pages):
    results = []
    for page in range(1, pages+1):
        url = f"https://api.adzuna.com/v1/api/jobs/us/search/{page}"

        response = requests.get(url, params=params)
        data = response.json()
        results.extend(data['results'])

    return results


def format_job_list(data):
    jobs = []
    for i in data:
        job = {}

        job['id'] = i['id']
        job['title'] = i.get('title', '').replace(
            '\u272a', '').replace('\u200b', '')
        job['company'] = i['company'].get('display_name', '').replace(
            '\u272a', '').replace('\u200b', '')
        job['url'] = i['redirect_url']
        jobs.append(job)

    return jobs
