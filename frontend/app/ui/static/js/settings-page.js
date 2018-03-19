$(document).ready(function() {
    // Submit username change
    $('#change-username').submit(function(event) {
        // Clear error text
        $('#username-error-text').empty();

        // Check if username is in use
        console.log('Checking if username is available.');
        let usernameGet = $.get('/username', { username: $('#username').val() }, function(data) {
            // If username is not taken, change it
            if(!data.taken) {
                console.log('Username is available, changing...');
                $.put('/changeDisplayName', { place: 'holder' });
            } else {
                // Username is taken, display error message
                console.log('Username is unavailable.');
                $('#username-error-text').html('Username is taken.');
            }
        });

        // Log errors from previous request
        usernameGet.fail(function() {
            console.log('Could not check if username ' + $('#username').val() + ' is available.');
        });
    });

    // Submit profile picture change
    $('#change-profile-pic').submit(function(event) {

    });
});