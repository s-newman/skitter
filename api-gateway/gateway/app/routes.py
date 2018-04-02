from app import app
from app.config import *
from flask import request, Response, abort, redirect
import requests
from json import loads as json_to_dict
from sqlalchemy.engine import create_engine

CHUNK_SIZE = 1024
"""The size, in bytes, of data to stream at a time."""


@app.route('/logout')
def logout():
    cnx = connect_db()

    # Remove the user's session from the database
    cnx.execute('PREPARE remove_session FROM \
                 \'DELETE FROM SESSION WHERE session_id = ?\';')
    cnx.execute('SET @a = \'{}\';'.format(request.cookies.get('SID')))
    cnx.execute('EXECUTE remove_session USING @a;')
    
    # Return the logout page
    r = get_response(FRONTEND, request.path, 'GET')
    return make_response(r)


@app.route('/')
@app.route('/static/<filename>')
@app.route('/static/js/<filename>')
@app.route('/static/img/<filename>')
def frontend(page=None, filename=None):
    """Fetches a webpage from the frontend.

    :param page:        A string; the API endpoint for one of the frontend
                        pages (that does not include the index/home page).
    :param filename:    A string; the name of a static file on the server, such
                        as a javascript file or a stylesheet.
    :return:            The resultant page, streamed back to the client.
    """
    r = get_response(FRONTEND, request.path, 'GET')
    return make_response(r)


@app.route('/settings')
@app.route('/dashboard')
@app.route('/new-account')
@app.route('/profile/<user>')
def internal_frontend(user=None):
    cnx = connect_db()

    # Execute the query
    cnx.execute('PREPARE check_auth FROM \
                 \'SELECT * FROM SESSION WHERE session_id = ?\';')
    cnx.execute('SET @a = \'{}\';'.format(request.cookies.get('SID')))
    result = cnx.execute('EXECUTE check_auth USING @a;')
    
    # Convert the results to a list to make my life easier
    rows = [row for row in result]

    # Display a 401 error if the user is not logged in
    if len(rows) != 1:
        abort(401)
    else:
        # The user is logged in, allow them to continue
        r = get_response(FRONTEND, request.path, 'GET')
        return make_response(r)


@app.route('/isAuthenticated')
@app.route('/signIn', methods=['POST'])
@app.route('/newUser', methods=['POST'])
@app.route('/deleteUser')
def authentication():
    if request.method == 'GET':
        r = get_response(AUTH, request.full_path, 'GET')
    elif request.method == 'POST':
        r = get_response(AUTH, request.path, 'POST', request.data)

    return make_response(r)


def make_response(r):
    headers = dict(r.headers)

    def generate():
        for chunk in r.iter_content(CHUNK_SIZE):
            yield chunk
    return Response(generate(), headers=headers)


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
        return requests.get(url)

    elif http_method == 'POST':
        return requests.post(url, json=json_to_dict(data.decode('utf-8')))


# Optional methods are not included in this list.
@app.route('/changeDisplayName')
@app.route('/changeProfileImage')
@app.route('/AddSkit')
@app.route('/RemoveSkit')
@app.route('/GetSkits')
@app.route('/followUser')
@app.route('/unfollowUser')
@app.route('/userSearch')
@app.route('/addSkitReply')
@app.route('/removeSkitReply')
def unimplemented():
    """Returns an HTTP 501: Not Implemented error.

    Used as a placeholder for all API endpoints that have not been implemented.
    Once an endpoint is implemented, it should be moved from here into it's own
    function.

    :return:    An HTTP 501: Not Implemented error.
    """
    abort(501)


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
            print('Could not connect to database.  Message is: "{}". \
                   Retrying...'.format(e))
    print('Connected to database.')
    return cnx