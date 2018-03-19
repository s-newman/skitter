from locust import HttpLocust, TaskSet, task
from random import randint


class Tests(TaskSet):
    @task
    def index(self):
        self.client.get('/')

    @task
    def settings(self):
        self.client.get('/settings')

    @task
    def dashboard(self):
        self.client.get('/dashboard')

    @task
    def new_account(self):
        self.client.get('/new-account')


class WebsiteUser(HttpLocust):
    task_set = Tests
    min_wait = 1000
    max_wait = 10000
    host = 'http://localhost'
