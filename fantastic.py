import requests
import os
import csv


def find_jobs(query: str, ai_remote: str = None, ai_experience: str = None, limit: int = 10, file_name: str = 'jobs'):
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

    path = f'{file_name}.csv'
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
                    f'No new jobs found. Try expanding your search.')
        else:
            with open(path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames)

                writer.writeheader()
                writer.writerows(jobs)
    else:
        print(f'No jobs found. Try expanding your search.')


# test
# find_jobs('developer | \'software engineer\' | ((\'full stack\' | frontend | backend) & engineer)',
#           'Remote OK,Remote Solely', '0-2')
# developer | 'software engineer' | (('full stack' | frontend | backend) & engineer)
