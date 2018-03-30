# Skitter API Reference
This is a complete reference of all Skitter API nodes for developers and the
curious.

All nodes are named in the format `METHOD /node/uri`.  Requests to nodes should
be formatted as `METHOD https://skitter.com/node/uri`.

## Authentication and User Manipulation
API nodes that relate to the authentication, creation, and removal of users.

### GET     /isAuthenticated
__Not implemented__
Checks if a specific user is currently authenticated, given their username and password.

### POST    /signIn
__Not implemented__
Attempts to authenticate a specific user.

### PUT     /logout
__Not implemented__
Attempts to log out a specific user.

### POST    /newUser
__Not implemented__
Registers a new user.

### GET     /deleteUser
__Not implemented__
Deletes an already existing user.

## Settings
API nodes that relate to the viewing and modification of user settings.

### GET     /username
__Not implemented__
Checks if a specific username/display name is taken.  This function is rate-limited.

#### Parameters:
```
{
    username: 'The username to test'
}
```

#### Returns:
```
{
    taken: boolean value
}
```
`taken` is `true` if the username is taken, and `false` if the username is free.

### PUT     /changeDisplayName
__Not implemented__
Changes a user's display name.

### PUT     /changeProfileImage
__Not implemented__
Changes a user's profile image.

### GET     /userInfo
__Not implemented__
Retrieves the username and profile picture for a user.

### GET     /settings
__Not implemented__
Retrieves the current account settings for a specific user.

## Skits and Replies
API nodes that relate to the creation, removal, and viewing of Skits and
replies to Skits.

### POST    /addSkit
__Not implemented__
Creates a new Skit.

### DELETE  /removeSkit
__Not implemented__
Deletes an existing Skit.

### GET     /getSkits
__Not implemented__
Retrieves the latest Skits from all followed users.

### POST    /addSkitReply
__Not implemented__
Creates a new reply to a Skit.

### DELETE  /removeSkitReply
__Not implemented__
Deletes an existing reply to a skit.

### GET     /getSkitReplies
__Not implemented__
Retrieves the replies to a Skit.

## Following Users
API nodes that relate to following and unfollowing users.

### GET     /userSearch
__Not implemented__
Retrieves the results of a user search.

### PUT     /followUser
__Not implemented__
Follows a user.

### DELETE  /unfollowUser
__Not implemented__
Unfollows a user.
