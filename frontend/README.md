# Skitter Frontend
This is the microservice that handles the user interface for Skitter.  It is
built on a Flask application to make writing consistent HTML pages simpler and
easier.

## Testing
There are two different ways of testing the application, depending on your
goal.

### Flask development webserver
The webserver packaged with Flask is sufficient for development work and
testing, but should not be used in production.  To test this configuration, run
the following commands from this directory:
```
cd app
pip install -r requirements.txt
export FLASK_APP=run.py
flask run
```
This will run the frontend webserver at `localhost:5000`.

### Flask as uWSGI application with nginx webserver
While Flask's packaged webserver is simple and easy to set up, it is not
appropriate for production use.  To test the frontend portion of the
environment that will be used in production, run the following command:
```
sudo docker-compose up
```
This will run the frontend webserver at `localhost`.
