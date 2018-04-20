from following import app
from following.utils import *
from flask import request, abort, jsonify
from json import loads


@app.route('/userSearch')
def search():
    # Parse the search string
    keywords = request.args['search_string'].split(' ')

    cnx = connect_db()
    data = {'users': []}

    # Search for each keyword
    for keyword in keywords:
        if keyword == '':
            # You're trying to scam us.  Get the heck outta here.
            continue

        cnx.execute('PREPARE get_results FROM \'SELECT\n' +
                    'USER_INFO.rit_username,\n' +
                    'USER_INFO.first_name,\n' +
                    'USER_INFO.last_name,\n' +
                    'PROFILE_PICTURE.picture\n' +
                    'FROM USER_INFO INNER JOIN PROFILE_PICTURE\n' +
                    'ON USER_INFO.profile_picture_id = ' +
                    'PROFILE_PICTURE.picture_id\n' +
                    'WHERE (\n' +
                    'rit_username LIKE ?\n' +
                    'OR first_name LIKE ?\n' +
                    'OR last_name LIKE ?)\';')
        cnx.execute('SET @a = \'%{}%\';'.format(keyword))
        cnx.execute('SET @b = \'%{}%\';'.format(keyword))
        cnx.execute('SET @c = \'%{}%\';'.format(keyword))
        results = [r for r in cnx.execute('EXECUTE get_results USING ' +
                                          '@a, @b, @c;')]
        for result in results:
            user = {
                'rit_username': result[0],
                'first_name': result[1],
                'last_name': result[2],
                'profile_picture': result[3]
            }
            if user not in data['users']:
                data['users'].append(user)

    # Quietly limit the number of results
    data['users'] = data['users'][:50]

    # Close the database connection
    cnx.close()

    # Prepare the results and return them
    return jsonify(data)


@app.route('/followUser')
def follow():
    # Parse the request data
    data = loads(request.data.decode('utf-8'))

    cnx = connect_db()

    # Check that the user is logged in
    cnx.execute('PREPARE check_auth FROM ' +
                '\'SELECT * FROM SESSION WHERE session_id = ?\';')
    cnx.execute('SET @a = \'{}\';'.format(data['session_id']))
    results = [r for r in cnx.execute('EXECUTE check_auth USING @a;')]
    
    # There should only be one entry for that session ID
    if len(results) != 1:
        return jsonify({'success':False})
    
    # Save the username
    username = results[0][0]

    # Check if the user is already followed
    cnx.execute('PREPARE check_follow FROM ' +
                '\'SELECT * FROM FOLLOW\n' +
                'WHERE follower = ? AND followed = ?\';')
    cnx.execute('SET @a = \'{}\';'.format(username))
    cnx.execute('SET @b = \'{}\';'.format(data['rit_username']))
    results = [r for r in cnx.execute('EXECUTE check_follow USING @a, @b;')]
    if len(results) > 0:
        return jsonify({'success':True})

    # Follow the user if they aren't followed yet
    cnx.execute('PREPARE follow_user FROM ' +
                '\'INSERT INTO FOLLOW VALUES (?, ?)\';')
    cnx.execute('SET @a = \'{}\';'.follow(username))
    cnx.execute('SET @b = \'{}\';'.follow(data['rit_username']))
    cnx.execute('EXECUTE follow_user USING @a, @b;')
    cnx.execute('COMMIT;')
    cnx.close()
    return jsonify({'success':True})


@app.route('/unfollowUser')
def unfollow():
    return None
