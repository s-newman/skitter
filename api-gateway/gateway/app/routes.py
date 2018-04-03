from app import app
from app.config import *
from app.utils import *
from flask import request, abort
import requests
from json import loads as json_to_dict

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

    # Close database connection
    cnx.close()

    # Remove the cookie
    resp = get_response(FRONTEND, request.path, 'GET')
    resp.set_cookie('SID', value='', expires=0)

    # Return the logout page
    return resp


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
@app.route('/signIn', methods=['POST'])
@app.route('/newUser', methods=['POST'])
@app.route('/deleteUser')
def authentication():
    if request.method == 'GET':
        resp = get_response(AUTH, request.full_path, 'GET')
    elif request.method == 'POST':
        if request.path == '/signIn':
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
        else:
            # Posting something other than /signIn, so don't need to check for
            # test authentication
            resp = get_response(AUTH, request.path, 'POST', request.data)

    return resp


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
