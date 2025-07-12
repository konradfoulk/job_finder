import requests
import os
import csv

url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
params = {
    "app_id": "2468334f",
    "app_key": "30cac15e7cdfa5ba0e4d5ef0b26ae978",
    "results_per_page": 20,
    "what": "software developer",
    "max_days_old": 7
}

response = requests.get(url, params=params)
data = response.json()
results = data['results']

jobs = []
for i in results:
    job = {}
    job['id'] = i['id']
    job['title'] = i.get('title').replace('\u272a', '')
    job['company'] = i['company'].get('display_name').replace('\u272a', '')
    job['url'] = i.get('redirect_url')
    jobs.append(job)

path = 'jobs.csv'
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
        print('No new jobs found. Try expanding your search.')
else:
    if jobs:
        with open(path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames)

            writer.writeheader()
            writer.writerows(jobs)
    else:
        print('No jobs found. Try expanding your search.')
