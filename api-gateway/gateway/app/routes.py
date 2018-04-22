from app import app
from app.config import *
from app.utils import *
from flask import request, abort
import requests
from json import loads as json_to_dict
from json import dumps

CHUNK_SIZE = 1024
"""The size, in bytes, of data to stream at a time."""


@app.route('/logout')
def logout():
    cnx = connect_db()

    # Remove the user's session from the database
    cnx.execute('PREPARE remove_session FROM ' +
                '\'DELETE FROM SESSION WHERE session_id = ?\';')
    cnx.execute('SET @a = \'{}\';'.format(request.cookies.get('SID')))
    cnx.execute('EXECUTE remove_session USING @a;')
    cnx.execute('COMMIT;')

    # Close database connection
    cnx.close()

    # Remove the cookie
    resp = get_response(FRONTEND, request.path, 'GET')
    resp.set_cookie('SID', value='', expires=0)

    # Return the logout page
    return resp


@app.route('/')
@app.route('/search')
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
    return get_response(FRONTEND, request.path, 'GET')


@app.route('/settings')
@app.route('/dashboard')
@app.route('/new-account')
@app.route('/profile/<user>')
def internal_frontend(user=None):
    cnx = connect_db()

    # Check if the user is authenticated
    cnx.execute('PREPARE check_auth FROM ' +
                '\'SELECT * FROM SESSION WHERE session_id = ?\';')
    cnx.execute('SET @a = \'{}\';'.format(request.cookies.get('SID')))
    result = cnx.execute('EXECUTE check_auth USING @a;')

    # Convert the results to a list to make my life easier
    rows = [row for row in result]

    # Close database connection
    cnx.close()

    # Display a 401 error if the user is not logged in
    if len(rows) != 1:
        abort(401)
    else:
        # The user is logged in, allow them to continue
        return get_response(FRONTEND, request.path, 'GET')


@app.route('/isAuthenticated')
@app.route('/newUser', methods=['POST'])
@app.route('/deleteUser')
def authentication():
    if request.method == 'GET':
        resp = get_response(AUTH, request.full_path, 'GET')
    elif request.method == 'POST':
        resp = get_response(AUTH, request.path, 'POST', request.data)

    return resp


@app.route('/signIn', methods=['POST'])
def sign_in():
    # Check if we're using test authentication
    json_dict = json_to_dict(request.data.decode('utf-8'))
    if json_dict['username'] in TEST_USERS:
        # Test authentication is in use
        resp = test_auth(json_dict)
    else:
        # Test authentication is not in use
        resp = get_response(AUTH, request.path, 'POST', request.data)
        # Add Session ID cookie to browser
        sid = json_to_dict(resp.get_data().decode())['sessionID']
        resp.set_cookie('SID', value=sid)

    # Convert response data to dict
    resp_data = json_to_dict(resp.get_data().decode())

    # Check if user has an account
    cnx = connect_db()
    cnx.execute('PREPARE check_user FROM ' +
                '\'SELECT * FROM USER_INFO WHERE rit_username = ?\';')
    cnx.execute('SET @a = \'{}\';'.format(json_dict['username']))
    rows = [row for row in cnx.execute('EXECUTE check_user USING @a;')]

    # If user doesn't have an account, set message
    if len(rows) == 0:
        resp_data['successful'] = 'user not created'

    # Add a CSRF token if the user is authenticated
    if resp_data['successful'] != 'false':
        resp.set_cookie('csrfToken', gen_secure_token())

    # Re-set the response data
    resp.set_data(dumps(resp_data).encode('utf-8'))

    return resp


@app.route('/followUser', methods=['POST'])
@app.route('/userSearch')
@app.route('/unfollowUser')
@app.route('/followState')
@app.route('/following')
def follow():
    if request.method == 'GET':
        resp = get_response(FOLLOW, request.full_path, 'GET',
                            cookies=request.cookies)
    elif request.method == 'POST':
        resp = get_response(FOLLOW, request.path, 'POST', request.data)

    return resp


@app.route('/changeProfileImage.php')
def profPic():
    return get_response(SETTINGS, request.path, 'POST', request.data)


@app.route('/img/<file>')
def images(file):
    return get_response(SETTINGS, request.full_path, 'GET')


# Optional methods are not included in this list.
@app.route('/AddSkit')
@app.route('/RemoveSkit')
@app.route('/GetSkits')
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
