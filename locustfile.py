from locust import HttpLocust, TaskSet
from random import randint

def index(l):
    l.client.get('/')

def settings(l):
    l.client.get('/settings')

def dashboard(l):
    l.client.get('/dashboard')

def new_account(l):
    l.client.get('/new-account')

class UserBehavior(TaskSet):
    tasks = {
        index: 1
    }

    def on_start(self):
        index(self)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
    host = 'http://localhost'
