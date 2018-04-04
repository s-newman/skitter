from csv import DictReader
from sys import exit
from subprocess import call

CSV_FILE = 'results'

call(['locust', '-f', 'testing/locustfile.py', '--csv=' + CSV_FILE, '--no-web',
      '-c', '100', '-r', '50', '-t', '1m', '--only-summary'])

reader = None

with open(CSV_FILE + '_requests.csv') as csvfile:
    reader = DictReader(csvfile)
    for row in reader:
        if row['Name'] == 'Total':
            if int(row['# failures']) * 100 > int(row['# requests']):
                exit(row['# failures'])
            else:
                exit(0)

call(['rm', '*.csv'])
