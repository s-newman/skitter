FRONTEND = 'front-proxy:8000'

AUTH = 'auth:8080'

DB = 'user-db:3306'

DB_USER = 'api-gateway'

DB_PASS = 'changemeplease-securitysucks'

FOLLOW = 'follow-proxy:8000'

SETTINGS = 'settings:80'

NODE_SERVER = 'skits-controller:8080'

RAILS_SERVER = 'skits-reply-controller:3000'

KIBANA = 'kibana:5601'

TEST_USERS = ['test{}'.format(idx) for idx in range(999)]

ORIGIN = 'http://localhost'

REFERER = 'http://localhost/'

HOST = 'localhost'
