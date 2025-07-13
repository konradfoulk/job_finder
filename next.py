import requests
import os
import csv


def find_jobs(query: str, query_not: str = '', pages: int = 1, age: int = 7):
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

    jobs = []
    for page in range(1, pages+1):
        url = f"https://api.adzuna.com/v1/api/jobs/us/search/{page}"

        response = requests.get(url, params=params)
        data = response.json()
        results = data['results']

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


find_jobs('junior software engineer', 'senior Senior sr sr. Sr Sr.', 10)

# find_jobs finds jobs for the us and outputs a CSV file as well as statuses for failed searches
# can easily script multiple searches by adding multiple funtion calls
