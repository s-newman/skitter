$(document).ready(function () {
    // Attempt to log in the user when they submit the login form
    $('#loginForm').submit(function() {
        if(authenticate()) {
            window.location.href = '/dashboard';
        }
        event.preventDefault();
    });
    
    $('#sign-up').click(function(event) {
        if(authenticate()) {
            console.log('signing up...');
            window.location.href = '/new-account';
        }
        event.preventDefault();
    });
});

function authenticate() {
    // Check if the user is already authenticated
    let authCheck = JSON.stringify({
        username: $('#username').val()
    });
    postJSON('/isAuthenticated', authCheck, function(data) {
        // Already authenticated, return
        if(data.authenticated === 'true') {
            return true;
        }
        // PLS FIX DUC THX
    });

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
            return true;
        }
    
        // Authentication failed
        else {
            $('#errorText').html('Invalid credentials.');
            $('#username').addClass('error');
            $('#password').addClass('error');
            console.log('Login attempt failed.');
            return false;
        }
    }, function() {
        // The thing failed.
        console.log('There was an error with your request.');
        return false;
    });
}

// Redirect all authenticated users
function authedUser() {
    window.location.href = '/dashboard';
}