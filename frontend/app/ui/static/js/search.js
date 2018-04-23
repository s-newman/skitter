$(document).ready(function() {
    $('#search').submit(function(event) {
        event.preventDefault();

        // Make search request
        let getRequest = $.get('/userSearch?search_string=' + encodeURIComponent(event.target[0].value), function(data) {
            // Clear out search results
            $('#results').empty();

            // Iterate through each search result
            data.users.forEach(function(user) {
                $('#results').append(renderUser(
                    user.rit_username,
                    user.first_name,
                    user.last_name,
                    user.profile_picture
                ));
            });
        });

        // Handle the failure of the request
        getRequest.fail(function() {
            console.log('There was an error making your search request.');
        });
    });
});

/**
 * Renders an HTML view of a user and the user's information.
 * @param {string} username The RIT username of the user
 * @param {string} fname  The first name of the user
 * @param {string} lname The last name of the user
 * @param {string} pic_url The URL of the user's profile picture
 */
function renderUser(username, fname, lname, pic_url) {
    return '<section>' +
    '<img class="result-user" src=' + pic_url + ' alt="Profile Picture" height=64 width=64 />' +
    '<p class="display-name">' + fname + ' ' + lname + '</br>' +
    '<a class="username" href="/profile/' + username + '">@' + username + '</a></p>' +
    '</section>';
}