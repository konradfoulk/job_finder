from pydantic import BaseModel
from openai import OpenAI
import requests
import os
import csv
from bs4 import BeautifulSoup


class AiResponse(BaseModel):
    remote: bool
    experience: str


ai = OpenAI()


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
        search = query + ' not ' + query_not
    else:
        search = query

    return params, search


def get_jobs(params, pages):
    results = []
    for page in range(1, pages+1):
        url = f"https://api.adzuna.com/v1/api/jobs/us/search/{page}"

        response = requests.get(url, params=params)
        data = response.json()
        results.extend(data['results'])

    return results


# could use pydantic for this??
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


def output_to_csv(file_name, job_list, search):
    path = f'{file_name}.csv'
    if job_list:
        fieldnames = job_list[0].keys()
        if os.path.exists(path):
            new_jobs = []

            with open(path, 'r') as f:
                reader = csv.DictReader(f, fieldnames)
                existing_ids = [i['id'] for i in reader]

                for i in job_list:
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
                writer.writerows(job_list)
    else:
        print(f'No jobs found for {search}. Try expanding your search.')


def find_jobs(query: str, query_not: str = '', pages: int = 1, age: int = 7, name: str = 'jobs'):
    params, search = update_params(query, query_not, age)

    results = get_jobs(params, pages)
    jobs = format_job_list(results)
    output_to_csv(name, jobs, search)


def find_qualified_jobs(query: str, query_not: str = '', pages: int = 1, age: int = 7, name: str = 'jobs', ai_remote: bool = False, ai_experience: str = 'mid'):
    params, search = update_params(query, query_not, age)
    results = get_jobs(params, pages)

    for i in results:
        url = i['redirect_url']
        print(url)  # test
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        desc = str(soup.find(class_='adp-body'))

        response = ai.responses.parse(
            model="gpt-4.1-nano-2025-04-14",
            input=[
                {
                    'role': 'system',
                    'content': '''
                    Analyze this job description and determine whether it is a remote position and the experience level of the position. 
                    Use the strings "entry", "mid", or "senior" to describe the experience level.
                    '''
                },
                {
                    'role': 'user',
                    'content': f'{desc}'
                }
            ],
            text_format=AiResponse
        )

        print(response.output_parsed)

        # print(desc)
        # print('\n\n[ENDOFJOB]' + str(type(desc)))


find_qualified_jobs('Jr. Web Developer', pages=10)

# find_jobs finds jobs for the us and outputs a CSV file as well as statuses for failed searches
# can easily script multiple searches by adding multiple funtion calls
