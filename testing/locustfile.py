from locust import HttpLocust, TaskSet, task
from random import randint
from json import dumps


# Ensure that unauthenticated users get 401 errors for internal pages
class UnauthenticatedTests(TaskSet):
    @task
    def dashboard(self):
        internal_page(self, '/dashboard')

    @task
    def settings(self):
        internal_page(self, '/settings')
    
    @task
    def new_account(self):
        internal_page(self, '/new-account')
    
    @task
    def profile(self):
        page_id = randint(1, 1000)
        internal_page(self, '/profile/{}'.format(page_id))
    
    @task
    def exit(self):
        self.interrupt()


class InternalTests(TaskSet):

    def on_start(self):
        username = 'test{}'.format(randint(1, 500))
        self.client.get('/')
        self.client.get('/isAuthenticated?username={}'.format(username))
        self.client.post('/signIn', json=dumps({
            'username': username,
            'password': 'fakenews'
        }))
    
    @task
    def dashboard(self):
        self.client.get('/dashboard')
    
    @task
    def settings(self):
        self.client.get('/settings')
    
    @task
    def new_account(self):
        self.client.get('/new-account')
    
    @task
    def profile(self):
        page_id = randint(1, 1000)
        self.client.get('/profile/{}'.format(page_id))

    @task
    def logout(self):
        self.client.get('/logout')
        self.interrupt()


class Tests(TaskSet):
    tasks = {
        InternalTests: 7,
        UnauthenticatedTests: 2
    }

    @task(1)
    def index(self):
        self.client.get('/')
    


class WebsiteUser(HttpLocust):
    task_set = Tests
    min_wait = 1000
    max_wait = 10000
    host = 'http://localhost'


def internal_page(self, page):
    """Ensure that an unauthenticated user recieves a 401 error for internal
    pages
    
    Arguments:
        page {string} -- The URI of the page to check
    """

    with self.client.get(page, catch_response=True) as response:
        if response.status_code == 401:
            response.success()
        else:
            response.failure('Did not return 401 error.')
