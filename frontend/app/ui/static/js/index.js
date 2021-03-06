$(document).ready(function () {
    // Attempt to log in the user when they submit the login form
    $('#loginForm').submit(function(event) {
        event.preventDefault();
        authenticate(event, '/dashboard');
    });
});

function authenticate(event, location) {
    // Clear error
    $('#errorText').empty();
    $('#username').removeClass('error');
    $('#password').removeClass('error');

    // Check if the user is already authenticated
    let authCheck = {
        username: $('#username').val()
    };
    let checkRequest = $.get('/isAuthenticated', authCheck);

    // Request is successful
    checkRequest.done(function(data1) {
        console.log('/isAuthenticated request sent successfully.');

        // Already authentiated
        if(data1.authenticated === 'true') {
            console.log('Already authenticated!');
            window.location.href = location;
        } else {
            // Attempt to authenticate the user
            console.log('Not already authentiated, please hold')
            let auth = JSON.stringify({
                username: $('#username').val(),
                password: $('#password').val(),
                "g-recaptcha-response": $('#captcha').val()
            });
            let authRequest = $.ajax({
                type: 'POST',
                url: '/signIn',
                contentType: 'application/json',
                data: auth,
                // xhrFields: {
                //     withCredentials: true
                // }
            });

            // Request is successful
            authRequest.done(function(data2) {
                console.log('/signIn request was successful.');

                // Was able to sign in
                if(data2.successful === 'true') {
                    console.log('Signed in!');
                    window.location.href = location;
                } else if(data2.successful === 'user not created') {
                    // No user has been created yet - need to create one first
                    console.log('User not created.');

                    // Save first and last names as cookies
                    setCookie('firstname', data2.message.firstname);
                    setCookie('lastname', data2.message.lastname);
                    setCookie('username', $('#username').val());

                    // Redirect
                    window.location.href = '/new-account';
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