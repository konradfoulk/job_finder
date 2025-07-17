import requests


def update_params(query, query_not, age):
    params = {
        "app_id": "2468334f",
        "app_key": "30cac15e7cdfa5ba0e4d5ef0b26ae978",
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
