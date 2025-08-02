from dotenv import load_dotenv
from openai import OpenAI
from .adzuna_jobs import *
from bs4 import BeautifulSoup
from .models import AiResponse
from utils import output_to_csv

load_dotenv()  # load environment variables to use os.environ
ai = OpenAI()  # initialize OpenAI client


# one function to query Adzuna api and output jobs
def find_jobs(query: str, query_not: str = '', pages: int = 1, age: int = 7, file_name: str = 'jobs'):
    '''
    *The Adzuna API paginates it's results. Therefore, in order to get more results you must query more pages.
    Each page has a default number of results per page of 50. This is the maximum.
    '''
    params = update_params(query, query_not, age)

    results = get_jobs(params, pages)
    jobs = format_job_list(results)
    output_to_csv(file_name, jobs)

# queary api, qualify results using ai, output qualified jobs


def find_qualified_jobs(query: str, query_not: str = '', pages: int = 1, age: int = 7, file_name: str = 'ai_jobs', ai_remote: bool = False, ai_experience: str = 'mid'):
    params = update_params(query, query_not, age)
    results = get_jobs(params, pages)

    ai_results = []
    # loop through results and qualify using OpenAI api
    for i in results:
        # use beautiful soup to get page content for OpenAI to use
        url = i['redirect_url']
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        desc = str(soup.find(class_='adp-body'))
        content = 'Title: ' + i['title'] + ' ' + desc

        # query OpenAI api with GPT 4.1 mini and structured output
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

        # get values of ai response
        data = response.output_parsed
        remote = data.remote
        experience = data.experience.value

        if remote == ai_remote and experience == ai_experience:
            ai_results.append(i)

    jobs = format_job_list(ai_results)
    output_to_csv(file_name, jobs)


# find_jobs finds jobs for the us and outputs a CSV file as well as statuses for failed searches
# can easily script multiple searches by adding multiple funtion calls
