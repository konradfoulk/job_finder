import requests

# Define the API endpoint and parameters
url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
params = {
    "app_id": "2468334f",
    "app_key": "30cac15e7cdfa5ba0e4d5ef0b26ae978",
    "results_per_page": 10,
    "what": "software developer",
    "max_days_old": 7
}

# Make the GET request
response = requests.get(url, params=params)

# Check status and print results
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)
