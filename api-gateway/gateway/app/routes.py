from app import app
from app.config import *
from flask import request, Response, abort
import requests

CHUNK_SIZE = 1024
"""The size, in bytes, of data to stream at a time."""

@app.route('/')
@app.route('/dashboard')
@app.route('/new-account')
@app.route('/static/<filename>')
@app.route('/static/js/<filename>')
@app.route('/static/img/<filename>')
def frontend(page=None, filename=None):
    """Fetches a webpage from the frontend.

    :param page:        A string; the API endpoint for one of the frontend
                        pages (that does not include the index/home page).
    :param filename:    A string; the name of a static file on the server, such
                        as a javascript file or a stylesheet.
    :return:           The resultant page, streamed back to the client.
    """
    r = get_response(FRONTEND, request.path)
    headers = dict(r.headers)
    def generate():
        for chunk in r.iter_content(CHUNK_SIZE):
            yield chunk
    return Response(generate(), headers=headers)

def get_response(host, method):
    """Make a given request and return the associated response.

    :param host:    A string; the hostname of the microservice endpoint to send
                    the request to, including the destination port.  Should be
                    formatted like:
                        frontend:8000
    :param method:  A string; the API method to send to the microservice
                    endpoint.  This string SHOULD NOT include the leading
                    forward slash.  For example, a request to /login should be
                    passed as:
                        login
    :return:        The response recieved for the given request.  Uses
                    streaming to send back requests as they are received to the
                    client.
    """
    # TODO: add HTTPS support
    url = 'http://{}{}'.format(host, method)
    # Fetch the URL and stream it back
    #return requests.get(url, stream=True, params=request.args)
    return requests.get(url)

# Optional methods are not included in this list.
@app.route('/isAuthenticated')
@app.route('/signIn')
@app.route('/newUser')
@app.route('/deleteUser')
@app.route('/changeDisplayName')
@app.route('/changeProfileImage')
@app.route('/logout')
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
