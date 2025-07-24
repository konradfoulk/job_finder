# Job Finder
### Output a CSV of job listings with a Python script using job search engine and job database APIs.
[Key Features](#key-features), [Download](#download), [Configuratoin](#configuration), [How to use](#how-to-use)

This project will create or append a list of jobs sourced from the Adzuna or Fantastic.jobs APIs to a new or existing CSV file. With the scripts provided, you can search for jobs using relevant keywords, automatically qualify jobs with AI, and view the results in a simple spreadsheet to start your job search and make it easy.

---
### Key Features

Keywords

- Search for key words in the job title.

Anti-keywords

- Filter for keywords you **don't** want as well as the ones you do.

Results

- Tailor the number of results you want using pages with Adzuna and results with Fantastic.jobs
- The defualt is one page (50 results) for Adzuna and 10 results for Fantastic.jobs

CSV file name

- Choose the name of a file that already exists to append your results or set the name for your new job search spreadsheet
- The default is "jobs.csv"

AI qualification

- Use the AI parameters to qualify each posting for you so you don't have to sift through the results yourself.

---
### Download

To download this project, simply clone this repository onto your local machine.

---
### Configuration

In order for your script to work, you'll need to do some configuration with the APIs yourself. This project uses the Adzuna, Fantastic.jobs, and OpenAI APIs to work. In order to use them yourself, you'll need to go to each of those organizations and get an API key and an app ID (for Adzuna only). Once you have your API keys and your Adzuna app ID, write each value to a `.env` file as follows:

```
OPENAI_API_KEY=your_api_key
adzuna_app_id=your_app_key
adzuna_app_key=your_api_key
fantastic_x-rapidapi-key=your_api_key
```

Make sure the `.env` file is in the root folder of the repository and your code the scripts will work perfectly.

---
### How to use
To run the project, simply navigate to the main.py file, and run the file with one or more of the following functions:
```python
adzuna.find_jobs('keywords')
fantastic.find_jobs('keywords')
```
To AI qualify your results, use `adzuna.find_qualified_jobs('keywords')` or `fantastic.find_jobs()` using the AI parameters

#### Keywords:

For Adzuna, multiple keywords may be space seperated. More information can be found in the Adzuna developer documentation [here](https://developer.adzuna.com/activedocs#!/adzuna/search).

The Fantastic.jobs script uses their `advanced_title_filter`. This allows for more functionality and better searches, but is more complicated. See their [documentation](https://rapidapi.com/fantastic-jobs-fantastic-jobs-default/api/active-jobs-db) for more information.

#### AI parameters:

|                  | Adzuna (.find_qualified jobs)                         | Fantastic.jobs                                                                     |
| ---------------- | ----------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Remote status    | `ai_remote` parameter `True` or `False`               | `ai_remote` parameter `"On-site"`,`"Hybrid"`,`"Remote OK"`,`"Remote Solely"`, delimit by `,` to filter for multiple job types |
| Experience Level | `ai_experience` parameter `"entry"`, `"mid"`, or `"senior"` | `ai_experience` parameter `"0-2"`,`"2-5"`,`"5-10"`,`"10+"`, delimit by `","` to filter for multiple job types |
|                  |                                                       | See the [Fantasic.jobs](https://rapidapi.com/fantastic-jobs-fantastic-jobs-default/api/active-jobs-db) documentation for more details |


#### Other parameters:

Additional functionality is accessed by utilizing the additional parameters in the `find_jobs()` and `find_qualified_jobs()` functions.

To filter for keywords you don't want:
- Use the `query_not` parameter with Adzuna and the `advanced_title_filter` format in the query for Fantastic.jobs

To set the number of results:
- Use the `pages` parameter with Adzuna and the `limit` parameter with Fantastic.jobs

To filter for the age of listings:
- Fantastic.jobs only returns listings that are a week old or younger, but use the `age` parameter with Adzuna to filter for oldest you want the results to be.

To set the name of the CSV output:
- Use the `name` parameter **without** the file extension
- For example if you want to create a file called `jobs.csv` or have an existing file by that name that you want to append the results to, simply input `jobs` into this parameter.

Writing results:

- If appending to an existing file, expect that the file should be formatted properly following the standards of a newly generated file in order for it to make sense.