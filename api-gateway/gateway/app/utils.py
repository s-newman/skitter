from app.config import *
from flask import make_response, jsonify, request
from werkzeug.datastructures import Headers
import requests
from json import loads as json_to_dict
from sqlalchemy.engine import create_engine, Connection
from sqlalchemy.pool import NullPool
from binascii import hexlify
from os import urandom


def get_response(host, method, http_method, data=None, cookies=None):
    """Make a given request and return the associated response.

    Arguments:
        host {string} -- The hostname of the microservice endpoint to send the
        request to, including the destination part.  Should be formatted as
        [hostname]:[port].  If parameters are included in the request (for
        example, in the case of a GET request), they should be included in the
        string.
        method {string} -- The API method the request is being sent to.
        http_method {string} -- The HTTP method to use to send the request to
        the microservice endpoint.
        cookies {dict} -- A dictionary of cookies to include in the request.

    Keyword Arguments:
        data {string} -- The message-body of the request.  Should only be set
        if the request method is POSt. (default: {None})

    Returns:
        flask.Response -- A response object that can be returned from a Flask
        view directly, or edited before returning.
    """

    # TODO: add HTTPS support
    url = 'http://{}{}'.format(host, method)
    # Fetch the URL and stream it back
    # return requests.get(url, stream=True, params=request.args)
    if http_method == 'GET':
        r = requests.get(url, cookies=cookies)

    elif http_method == 'POST':
        r = requests.post(url, json=json_to_dict(data.decode('utf-8')),
                          cookies=cookies)

    # Create a flask response object from the requests.Reponse object.  That's
    # not confusing, right?
    resp = make_response(r.content)
    headers = dict(r.headers)
    resp.headers.extend(headers)
    resp.status_code = r.status_code
    return resp


def test_auth(creds):
    """Performs authentiation for test users, such as "test123".

    Arguments:
        creds {dict} -- A dictionary containing the "username" and "password"
        keys that should be used to authenticate the test user.

    Returns:
        string -- A JSON stringified dictionary that can be returned in the
        message body of a response.  If the user is authenticated, it contains
        a header that will set the session cookie in the browser.
    """

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
                'successful': 'already authenticated'
            })

        # Generate the session ID
        sid = gen_secure_token()

        # Store the session ID in the session table
        cnx.execute('PREPARE add_session FROM ' +
                    '\'INSERT INTO SESSION (rit_username, session_id) ' +
                    'VALUES (?, ?)\';')
        cnx.execute('SET @a = \'{}\';'.format(creds['username']))
        cnx.execute('SET @b = \'{}\';'.format(sid))
        cnx.execute('EXECUTE add_session USING @a, @b;')
        cnx.execute('COMMIT')

        # Close the database connection
        cnx.close()

        # Emulate the auth server
        resp = jsonify({
            'sessionID': sid,
            'message': {
                'firstname': 'Test',
                'lastname': 'User'
            },
            'successful': 'true'
        })
        resp.set_cookie('SID', value=sid)
    else:
        # User isn't valid
        resp = jsonify({
            'sessionID': '',
            'message': 'Authentication error',
            'successful': 'false'
        })

    return resp


def connect_db():
    """Creates a new connection to the user database.

    Returns:
        sqlalchemy.engine.Connection -- A new connection object that is
        attached to the users table in the user database.
    """

    # Create engine
    engine = create_engine('mysql+mysqlconnector://{}:{}@{}/users'.format(
        DB_USER, DB_PASS, DB
    ), poolclass=NullPool)

    # Try to connect
    cnx = None
    while cnx is None:
        try:
            cnx = engine.connect()
        except Exception as e:
            print('Could not connect to database.  Message is: "{}". ' +
                  'Retrying...'.format(e))
    return cnx


def gen_secure_token():
    """Generates a secure token that is suitable for use as a session ID or in
    CSRF protections.

    Returns:
        string -- A 70-character ASCII string of hex characters that represents
        a cryptographically secure random 30-byte value.
    """

    return hexlify(urandom(30)).decode('ascii')


def csrf_check(request):
    """Verifies a state-changing request by verifying the request is same
    origin and that the CSRF token is valid.  The CSRF token in question is
    using the double cookie submit method.

    Arguments:
        request {flask.request} -- The request whose intent should be verified.

    Returns:
        boolean -- True if the request is valid, false if the request is
        invalid.
    """

    # Verify source origin
    source = (
        request.headers.get('Origin') == ORIGIN or
        request.headers.get('Referer').startswith(REFERER)
    )

    # Verify target origin
    target = request.headers.get('Host') == HOST

    # Verify token
    json_dict = json_to_dict(request.data.decode('utf-8'))
    token = json_dict['crsfToken'] == request.cookies.get('csrfToken')

    return source and target and token
