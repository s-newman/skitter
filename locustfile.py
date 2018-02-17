from locust import HttpLocust, TaskSet
from random import randint

def index(l):
    l.client.get('/')

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
