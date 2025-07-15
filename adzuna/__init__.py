from openai import OpenAI
from adzuna_jobs import *
from bs4 import BeautifulSoup
from models import AiResponse

ai = OpenAI()


def find_jobs(query: str, query_not: str = '', pages: int = 1, age: int = 7, name: str = 'jobs'):
    params = update_params(query, query_not, age)

    results = get_jobs(params, pages)
    jobs = format_job_list(results)
    output_to_csv(name, jobs)


def find_qualified_jobs(query: str, query_not: str = '', pages: int = 1, age: int = 7, name: str = 'ai_jobs', ai_remote: bool = False, ai_experience: str = 'mid'):
    params = update_params(query, query_not, age)
    results = get_jobs(params, pages)

    ai_results = []
    for i in results:
        url = i['redirect_url']
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        desc = str(soup.find(class_='adp-body'))
        content = 'Title: ' + i['title'] + ' ' + desc

        response = ai.responses.parse(
            model="gpt-4.1-mini-2025-04-14",
            input=[
                {
                    'role': 'system',
                    'content': 'Analyze this job description and determine whether it is a remote position and the experience level of the position.'
                },
                {
                    'role': 'user',
                    'content': f'{content}'
                }
            ],
            text_format=AiResponse
        )

        data = response.output_parsed
        remote = data.remote
        experience = data.experience.value

        if remote == ai_remote and experience == ai_experience:
            ai_results.append(i)

    jobs = format_job_list(ai_results)
    output_to_csv(name, jobs)


# test
# find_jobs('Jr. Web Developer', pages=10, name='adzuna_jobs')

# find_jobs finds jobs for the us and outputs a CSV file as well as statuses for failed searches
# can easily script multiple searches by adding multiple funtion calls
