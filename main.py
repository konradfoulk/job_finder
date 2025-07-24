import adzuna
import fantastic

# example scripts
adzuna.find_jobs('Jr. Web Developer', pages=10, name='adzuna_jobs')
fantastic.find_jobs('developer | \'software engineer\' | ((\'full stack\' | frontend | backend) & engineer)',
                    'Remote OK,Remote Solely', '0-2')
