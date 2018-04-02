from app.config import *
from flask import make_response, jsonify
from werkzeug.datastructures import Headers
import requests
from json import loads as json_to_dict
from sqlalchemy.engine import create_engine, Connection

def get_response(host, method, http_method, data=None):
    """Make a given request and return the associated response.

    :param host: A string; the hostname of the microservice endpoint to send
                 the request to, including the destination port.  Should be
                 formatted like:
                    frontend:8000
                 If parameters are included in the request (for example, in the
                 case of a GET request), they should be included in the string.
    :param method: A string; the API method to send to the microservice
                   endpoint.  This string SHOULD NOT include the leading
                   forward slash.  For example, a request to /login should be
                   passed as:
                        login
    :param http_method: A string; the HTTP method to use to send the request to
                        the microservice endpoint.
    :param data: A string; the body of the request.  Should only be set if the
                 request method is POST.
    :return: The response recieved for the given request.  Uses
             streaming to send back requests as they are received to the
             client.
    """
    # TODO: add HTTPS support
    url = 'http://{}{}'.format(host, method)
    # Fetch the URL and stream it back
    # return requests.get(url, stream=True, params=request.args)
    if http_method == 'GET':
        r = requests.get(url)

    elif http_method == 'POST':
        r = requests.post(url, json=json_to_dict(data.decode('utf-8')))
    
    # Create a flask response object from the requests.Reponse object.  That's
    # not confusing, right?
    resp = make_response(r.content)
    headers = dict(r.headers)
    resp.headers = Headers().extend(headers)
    resp.status_code = r.status_code
    return resp


def test_auth(creds):
    if creds['username'] in TEST_USERS and creds['password'] == 'fakenews':
        cnx = connect_db()

        # Check if authenticated
        cnx.execute('PREPARE check_session_dupe FROM ' +
                    '\'SELECT * FROM SESSION WHERE rit_username = ?\';')
        cnx.execute('SET @a = \'{}\';'.format(creds['username']))
        rows = [row for row in cnx.execute('EXECUTE check_session_dupe ' +
                                           'USING @a;')]

        # If authenticated, return the current SID
        if len(rows) == 1:
            return jsonify({
                'sessionID': rows[0][1],
                'message': {
                    'firstname': 'Test',
                    'lastname': 'User'
                },
                'successful': 'true'
            })

        # Generate the session ID
        sid = hexlify(urandom(30)).decode('ascii')

        # Store the session ID in the session table
        cnx.execute('PREPARE add_session FROM ' +
                    '\'INSERT INTO SESSION (rit_username, session_id) ' +
                    'VALUES (?, ?)\';')
        cnx.execute('SET @a = \'{}\';'.format(creds['username']))
        cnx.execute('SET @b = \'{}\';'.format(sid))
        cnx.execute('EXECUTE add_session USING @a, @b;')
        cnx.execute('COMMIT')

        # Emulate the auth server
        return jsonify({
            'sessionID': sid,
            'message': {
                'firstname': 'Test',
                'lastname': 'User'
            },
            'successful': 'true'
        })
    else:
        # User isn't valid
        return jsonify({
            'sessionID': '',
            'message': 'Authentication error',
            'successful': 'false'
        })


def connect_db():
    # Create engine
    engine = create_engine('mysql+mysqlconnector://{}:{}@{}/users'.format(
        DB_USER, DB_PASS, DB
    ))

    # Try to connect
    cnx = None
    while cnx is None:
        try:
            cnx = engine.connect()
        except Exception as e:
            print('Could not connect to database.  Message is: "{}". ' +
                  'Retrying...'.format(e))
    print('Connected to database.')
    return cnx