from app import app
from app.config import *
from app.utils import *
from flask import request, abort
import requests
import string
from json import loads as json_to_dict
from json import dumps
from datetime import datetime
from cgi import escape

CHUNK_SIZE = 1024
ALPHANUMERIC = string.ascii_letters + string.digits
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

@app.route('/addSkit', methods=['POST'])
@app.route('/removeSkit')
@app.route('/getSkits')
def skits_handler():
    if request.method == 'POST':
        # Add Skit: The front-end only send the content of the skit
        cnx = connect_db()
        SID = request.cookie.get('SID')
        cnx.execute('PREPARE check_auth FROM ' +
                        '\'SELECT * FROM SESSION WHERE session_id = ?\';')
        cnx.execute('SET @a = \'{}\';'.format(SID))
        results = [r for r in cnx.execute('EXECUTE check_auth USING @a;')]

        username = results[0][0]
        date_posted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = request.data['content']
        # Sanitize the first time
        if len(content) > 140:
            abort(406)
        content = escape(content)
        data = {
            "username": username,
            "date_posted": date_posted,
            "content": content
        }
        resp = get_response(NODE_SERVER, request.path, 'POST', data)
    elif request.method == 'GET':
        resp = get_response(NODE_SERVER, request.full_path, 'GET')
    return resp


@app.route('/addSkitReply', methods=['POST'])
@app.route('/removeSkitReply') #id
@app.route('/getSkitReplies') #skitID
def replies_handler():
    if request.method == 'POST':
        skitID = request.data['skitID']
        for c in skitID:
            if c not in ALPHANUMERIC:
                abort(406)
        resp = get_response(NODE_SERVER, '/getSkitById?id={}'.format(skitID), 'GET')
        if resp['success'] == 'false':
            abort(406)

        cnx = connect_db()
        SID = request.cookie.get('SID')
        cnx.execute('PREPARE check_auth FROM ' +
                        '\'SELECT * FROM SESSION WHERE session_id = ?\';')
        cnx.execute('SET @a = \'{}\';'.format(SID))
        results = [r for r in cnx.execute('EXECUTE check_auth USING @a;')]

        username = results[0][0]
        date_posted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content = request.data['content']

        # Sanitize the first time
        if len(content) > 140:
            abort(406)
        content = escape(content)
        data = {
            "username": username,
            "date_posted": date_posted,
            "content": content,
            "skitID": skitID
        }
        resp = get_response(NODE_SERVER, request.path, 'POST', data)
    elif request.method == 'GET':
        resp = get_response(NODE_SERVER, request.full_path, 'GET')

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


@app.route('/changeProfileImage.php', methods=['POST'])
def profPic():
    resp = make_response(requests.post(
        'http://settings/changeProfilePicture.php',
        data=request.data,
        files=request.files
    ).content)
    return resp


@app.route('/img/<file>')
def images(file):
    return get_response(SETTINGS, request.full_path, 'GET')


@app.route('/profilePicPath')
def path():
    cnx = connect_db()

    # Get user information
    cnx.execute('PREPARE get_info FROM ' +
                '\'SELECT * FROM USER_INFO WHERE rit_username = ?\';')
    cnx.execute('SET @a = \'{}\';'.format(request.args['username']))
    result = [row for row in cnx.execute('EXECUTE get_info USING @a;')]

    # Check if there is no user of that name
    if len(result) == 0:
        abort(404)
    else:
        result = result[0]

    # Get profile picture URL
    cnx.execute('PREPARE get_pic FROM ' +
                '\'SELECT * FROM PROFILE_PICTURE WHERE picture_id = ?\';')
    cnx.execute('SET @a = \'{}\';'.format(result[6]))
    picture_url = [r for r in cnx.execute('EXECUTE get_pic USING @a;')][0][1]

    return jsonify({'url': picture_url})


# Optional methods are not included in this list.
@app.route('/changeDisplayName')
@app.route('/changeProfileImage')
def unimplemented():
    """Returns an HTTP 501: Not Implemented error.

    Used as a placeholder for all API endpoints that have not been implemented.
    Once an endpoint is implemented, it should be moved from here into it's own
    function.

    :return:    An HTTP 501: Not Implemented error.
    """
    abort(501)
