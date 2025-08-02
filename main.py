import adzuna
import fantastic

# example scripts
adzuna.find_jobs('Jr. Web Developer', pages=10, file_name='exisitng_csv')
fantastic.find_jobs('developer | \'software engineer\' | ((\'full stack\' | frontend | backend) & engineer)',
                    'Remote OK,Remote Solely', '0-2', file_name='fantastic_jobs')
