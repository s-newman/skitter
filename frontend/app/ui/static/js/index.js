$(document).ready(function () {
    // Attempt to log in the user when they submit the login form
    $('#loginForm').submit(function(event) {
        event.preventDefault();
        authenticate(event, '/dashboard');
    });
    
    $('#sign-up').click(function(event) {
        event.preventDefault();
        authenticate(event, '/new-account');
    });
});

function authenticate(event, location) {
    // Clear error
    $('#errorText').empty();
    $('#username').removeClass('error');
    $('#password').removeClass('error');

    // Check if the user is already authenticated
    let authCheck = JSON.stringify({
        username: $('#username').val()
    });
    let checkRequest = postJSON('/isAuthenticated', authCheck);
    
    // Request is successful
    checkRequest.done(function(data) {
        console.log('/isAuthenticated request sent successfully.');

        // Already authentiated
        if(data.authenticated === 'true') {
            console.log('Already authenticated!');
            window.location.href = location;
        } else {
            // Attempt to authenticate the user
            console.log('Not already authentiated, please hold')
            let auth = JSON.stringify({
                username: $('#username').val(),
                password: $('#password').val()
            });
            let authRequest = postJSON('/signIn', auth);

            // Request is successful
            authRequest.done(function(data) {
                console.log('/signIn request was successful.');

                // Was able to sign in
                if(data.successful === 'true') {
                    console.log('Signed in!');
                    setCookie('SID', data.sessionID);
                    window.location.href = location;
                } else {
                    // Could not sign in
                    $('#errorText').html('Invalid credentials.');
                    $('#username').addClass('error');
                    $('#password').addClass('error');
                    console.log('Login attempt failed.');
                }
            });

            // Request is not successful
            authRequest.fail(function() {
                console.log('/signIn request was not successful.');
            });
        }
    });
    
    checkRequest.fail(function() {
        console.log('/isAuthenticated request was unsuccessful.');
    });
}

// Redirect all authenticated users
function authedUser() {
    window.location.href = '/dashboard';
}