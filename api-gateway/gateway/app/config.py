FRONTEND = 'front-proxy:8000'

AUTH = 'auth:8080'

DB = 'user-db:3306'

DB_USER = 'api-gateway'

DB_PASS = 'changemeplease-securitysucks'

TEST_USERS = ['test{}'.format(idx) for idx in range(500)]
