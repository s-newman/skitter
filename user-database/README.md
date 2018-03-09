# Skitter User Database
This is the microservice that stores all user information for Skitter.  All
queries should interface *only* with the API gateway.

## Testing
Testing the database is simple!  Just run:
```
sudo docker build -t user-db .
sudo docker run -p 3306:3306 -t user-db
```
And connect to the server with your client of choice.
