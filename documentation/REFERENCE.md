# Skitter API Reference
This is a complete reference of all Skitter API nodes for developers and the
curious.

All nodes are named in the format `METHOD /node/uri`.  Requests to nodes should
be formatted as `METHOD https://skitter.com/node/uri`.

## Authentication and User Manipulation
API nodes that relate to the authentication, creation, and removal of users.

### GET     /user/auth-state
__Not implemented__
Checks if a specific user is currently authenticated.

### PUT     /user/logged-in
__Not implemented__
Attempts to authenticate a specific user.

### PUT     /user/logged-out
__Not implemented__
Attempts to log out a specific user.

### POST    /user/new
__Not implemented__
Registers a new user.

### DELETE  /user
__Not implemented__
Deletes an already existing user.

## Settings
API nodes that relate to the viewing and modification of user settings.

### PUT     /account/display-name
__Not implemented__
Changes a user's display name.

### PUT     /account/profile-image
__Not implemented__
Changes a user's profile image.

### GET     /account/settings
__Not implemented__
Retrieves the current account settings for a specific user.

## Skits and Replies
API nodes that relate to the creation, removal, and viewing of Skits and
replies to Skits.

### POST    /skit/new
__Not implemented__
Creates a new Skit.

### DELETE  /skit
__Not implemented__
Deletes an existing Skit.

### GET     /skit/followed
__Not implemented__
Retrieves the latest Skits from all followed users.

### POST    /skit/reply/new
__Not implemented__
Creates a new reply to a Skit.

### DELETE  /skit/reply
__Not implemented__
Deletes an existing reply to a skit.

### GET     /skit/reply
__Not implemented__
Retrieves the replies to a Skit.

## Following Users
API nodes that relate to following and unfollowing users.

### GET     /search-results/user
__Not implemented__
Retrieves the results of a user search.

### PUT     /followed-user/new
__Not implemented__
Follows a user.

### DELETE  /followed-user
__Not implemented__
Unfollows a user.

## Other
API nodes that don't fall under any other category.

### POST    /mysql-query
__Not implemented__
Makes a query to the MySQL database.
