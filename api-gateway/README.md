# Skitter API Gateway
This is the microservice that serves as the "brain" of Skitter.  All requests
and responses are handled by the gateway, and the bulk of the security checks
are also processed here.

## Testing
The API gateway is not really meant to be tested by itself.  It works in
conjunction with the microservice endpoints, and running a standalone version
of it is basically useless.  That said, if you *really* want to test it by
itself, you've come to the right place.

### Standalone API Gateway
To test the API Gateway by itself, run the following commands:
```
pip install -r requirements.txt
export FLASK_APP=run.py
flask run
```

## API Gateway with nginx proxy
To test the API Gateway with an nginx proxy initially catching all requests,
run the following command:
```
sudo docker-compose up
```
