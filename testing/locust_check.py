from csv import DictReader
from sys import exit
from subprocess import call

CSV_FILE = '../results'

call(['locust', '-f', 'locustfile.py', '--csv=' + CSV_FILE, '--no-web', '-c',
      '300', '-r', '50', '-t', '1m'])

reader = None

with open(CSV_FILE + '_requests.csv') as csvfile:
    reader = DictReader(csvfile)
    for row in reader:
        if row['Name'] == 'Total':
            exit(int(row['# failures']))

call(['rm', '*.csv'])
