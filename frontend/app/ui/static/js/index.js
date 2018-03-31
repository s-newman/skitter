$(document).ready(function () {
    // Attempt to log in the user when they submit the login form
    $('#loginForm').submit(function(event) {
        // Clear error
        $('#errorText').empty();
        $('#username').removeClass('error');
        $('#password').removeClass('error');
        
        // Create JSON string to send
        let postData = JSON.stringify({
            username: $('#username').val(),
            password: $('#password').val()
        });
        console.log('Attempting to authenticate user:', postData);

        // Attempt to authenticate
        postJSON('/signIn', postData, function(data) {
            // Authentication was successful
            if(data.successful === 'true') {
                console.log('Authentication successful.');
                setCookie('SID', data.sessionID, 1);
                authedUser();
            }

            // Authentication failed
            else {
                $('#errorText').html('Invalid credentials.');
                $('#username').addClass('error');
                $('#password').addClass('error');
                console.log('Login attempt failed.');
            }
        }, function() {
            // The thing failed.
            console.log('There was an error with your request.');
        });

        event.preventDefault();
    });

    $('#sign-up').click(function(event) {
        // We don't want the form to be submitted (yet)!
        event.preventDefault();
        console.log('signing up...');
        window.location.href = '/new-account';
    });
});

// Redirect all authenticated users
function authedUser() {
    window.location.href = '/dashboard';
}