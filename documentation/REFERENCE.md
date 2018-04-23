# Skitter API Reference
This is a complete reference of all Skitter API nodes for developers and the
curious.

All nodes are named in the format `METHOD /node/uri`.  Requests to nodes should
be formatted as `METHOD https://skitter.com/node/uri`.

## Authentication and User Manipulation
API nodes that relate to the authentication, creation, and removal of users.

### `GET /isAuthenticated`
Checks if a specific user is currently authenticated, given their RIT username.

#### Parameters:
```
{
    username: The RIT username to check for authentication
}
```

#### Returns:
```
{
    authenticated: boolean value,
    message: string
}
```
- `authenticated`
    - `true` if the user is authenticated against the RIT LDAP server.
    - `false` if the user is not authenticated against the RIT LDAP server.
- `message`
    - An empty string (`""`) if no error occurred.
    - A non-empty string if any error occurred during the process of checking for authentication.

### `POST /signIn`
Attempts to authenticate a specific user using the RIT username.

#### Parameters:
```
{
    username: The username of the RIT user to log in as,
    password: The password of the RIT user to log in as
}
```

#### Returns:
```
{
    sessionID: The session ID,
    message: object or string,
    successful: boolean value
}
```
- `sessionID`
    - A new session ID of the logged in user if the autentication is successful.
    - An empty string (`""`) if the authentication is unsuccessful.
- `message`
    - If authentication is successful, `message` is the following object:
        ```
        {
            firstname: The RIT student first name,
            lastname: The RIT student last name
        }
        ```
    - If authentication is unsuccessful, `message` is a string describing the problem.
- `successful`
    - `"true"` when authentication is successful
    - `"false"` when authentication is unsuccessful.

### `PUT /logout`
__Not implemented__
Attempts to log out a specific user.

### `POST /newUser`
Registers a new user.

#### Parameters:
```
{

}
```

#### Returns:
```
{

}
```

### `GET /deleteUser`
Deletes an already existing user.

#### Parameters:
```
{

}
```

#### Returns:
```
{

}
```

## Settings
API nodes that relate to the viewing and modification of user settings.

### GET     /username
__Not implemented__
Checks if a specific username/display name is taken.  This function is rate-limited.

#### Parameters:
```
{
    username: The username to test
}
```

#### Returns:
```
{
    taken: boolean value
}
```
`taken` is `true` if the username is taken, and `false` if the username is free.

### POST     /changeProfileImage
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

### POST /addSkit
Creates a new Skit.

#### Parameters:
```
{
    username: The RIT username of the author,
    content: The content of the skit,
    date_posted: The timestamp of the skit for indexing purpose
}
```

#### Returns:
```
{
    successful: boolean,
    skit_id: string,
    message: string
}
```
- `successful`: `true` if the skit is successfully indexed, `false` otherwise.
- `skit_id`: a string represent the id of the document in the elasticsearch cluster if the skit was successfully index or an empty string otherwise.
- `message`: any error message will be in this field.

### DELETE /removeSkit
Deletes an existing Skit.

#### Parameters:
```
{

}
```

#### Returns:
```
{

}
```

### GET /getSkits
Retrieves the latest Skits from all followed users.

#### Parameters:
```
{

}
```

#### Returns:
```
{

}
```

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

#### Parameters:
```
{
    search_string: string
}
```
- `search_string`: A URL-encoded string to use for the search.

#### Returns:
```
{
    users: [
        {
            rit_username: string,
            first_name: string,
            last_name: string,
            profile_picture: string
        }
    ]
}
```
- `users`: A list of unique user information objects.
- `rit_username`: The RIT username for the given search result user.
- `first_name`: The first name for the given search result user.
- `last_name`: The last name for the given search result user.
- `profile_picture`: The URL to the user's profile picture image on the server.  Can be used to insert into a webpage.

### POST    /followUser
Uses the SID cookie.

#### Parameters:
```
{
    rit_username: string,
    session_id: string
}
```
- `rit_username`: The RIT username of the user that should be followed
- `session_id`: The session token of the currently logged-in user (this is the user doing the following)

#### Returns:
```
{
    success: boolean
}
```
- `success`: `True` if the user was added to the list of followed users, or if they already are followed.  `False` if there was an authentication error, or any other problems.

### GET     /unfollowUser

#### Parameters:
```
{
    unfollow: string
}
```
- `unfollow`: The RIT username of the person you would like to unfollow.

#### Returns:
```
{
    success: boolean
}
```
- `success`: `True` if the user was successfully unfollowed, otherwise `False`.

### GET     /followState
Uses the SID cookie.

#### Parameters:
```
{
    follow: string
}
```
- `follow`: The RIT username of the person you would like to check if you are following.

#### Returns:
```
{
    success: boolean
}
```
- `success`: `True` if the user is currently followed, `False` if the user is not followed.

### GET     /following
Uses the SID cookie.

#### Parameters:
None.

#### Returns:
```
{
    users: [
        rit_username: string,
        ...
    ]
}
```
- `users`: An array of usernames that the user is currrently following.  If there was an error, or if the user is not following any users, will be `None`.