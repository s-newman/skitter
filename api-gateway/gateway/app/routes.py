from app import app
from app.config import *
from flask import request, Response
import requests

CHUNK_SIZE = 1024
"""The size, in bytes, of data to stream at a time."""

@app.route('/')
@app.route('/ui/<page>')
@app.route('/static/<filename>')
def frontend(page=None, filename=None):
    """Fetches a webpage from the frontend.

    :param page:        A string; the API endpoint for one of the frontend
                        pages (that does not include the index/home page).
    :param filename:    A string; the name of a static file on the server, such
                        as a javascript file or a stylesheet.
    :returns:           The resultant page, streamed back to the client.
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
