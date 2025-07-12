import requests
import os
import csv


def find_jobs(query: str, query_not: str = '', n_results: int = 50, age: int = 7):
    # pages = n_results/50 -> round up

    url = "https://api.adzuna.com/v1/api/jobs/us/search/1"

    params = {
        "app_id": "2468334f",
        "app_key": "30cac15e7cdfa5ba0e4d5ef0b26ae978",
        "results_per_page": 50,
        "what": query,
        "max_days_old": age
    }

    if query_not:
        params['what_exclude'] = query_not
        search = query + ' not ' + query_not
    else:
        search = query

    response = requests.get(url, params=params)
    data = response.json()
    results = data['results']

    jobs = []
    for i in results:
        job = {}
        job['id'] = i['id']
        job['title'] = i.get('title', '').replace(
            '\u272a', '').replace('\u200b', '')
        job['company'] = i['company'].get('display_name', '').replace(
            '\u272a', '').replace('\u200b', '')
        job['url'] = i.get('redirect_url', '')
        jobs.append(job)

    path = 'jobs.csv'
    if jobs:
        fieldnames = jobs[0].keys()
        if os.path.exists(path):
            new_jobs = []

            with open(path, 'r') as f:
                reader = csv.DictReader(f, fieldnames)
                existing_ids = [i['id'] for i in reader]

                for i in jobs:
                    if i['id'] not in existing_ids:
                        new_jobs.append(i)

            if new_jobs:
                with open(path, 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames)

                    writer.writerows(new_jobs)
            else:
                print(
                    f'No new jobs found for {search}. Try expanding your search.')
        else:
            with open(path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames)

                writer.writeheader()
                writer.writerows(jobs)
    else:
        print(f'No jobs found for {search}. Try expanding your search.')


find_jobs('software engineer', 'senior sr sr. Senior Sr Sr.')
