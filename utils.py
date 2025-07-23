import os
import csv


# input formated job list
# output structured csv file with job list contents
def output_to_csv(file_name, job_list):
    path = f'{file_name}.csv'  # file name
    if job_list:
        fieldnames = job_list[0].keys()  # define column names
        # if file already exists only add new jobs
        if os.path.exists(path):
            new_jobs = []

            # read existing file, check job list against existing jobs, and add unique jobs to a seperate list
            with open(path, 'r') as f:
                reader = csv.DictReader(f, fieldnames)
                existing_ids = [i['id'] for i in reader]

                for i in job_list:
                    if i['id'] not in existing_ids:
                        new_jobs.append(i)

            # append new jobs to existing file
            if new_jobs:
                with open(path, 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames)

                    writer.writerows(new_jobs)
            else:
                print(
                    f'No new jobs found. Try expanding your search.')
        else:
            # write jobs to new file
            with open(path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames)

                writer.writeheader()
                writer.writerows(job_list)
    else:
        print(f'No jobs found. Try expanding your search.')
