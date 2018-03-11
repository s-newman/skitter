// Check if the user is authenticated already
let authCheckPost = $.post('/isAuthenticated', getCookie('SID'), function(data) {
    console.log('Checking if user is authenticated...');
    let response = JSON.parseJSON(data);
    if(response['status'] == 'authenticated') {
        // user is auth'd, redirect em
        console.log('User is authenticated, redirecting...');
        authedUser();
    }
});

$(document).ready(function () {
    // Attempt to log in the user when they submit the login form
    $('#loginForm').submit(function(event) {
        // Create JSON string to send
        let postData = {
            username: $('#username').val(),
            password: $('#password').val()
        };
        console.log('Attempting to authenticate user:', postData);

        // Attempt to authenticate
        let loginPost = $.post('/login', postData);

        // Log to console if request failed
        loginPost.fail(function() {
            console.log('Login attempt failed.');
        });

        // Redirect to dashboard page if request was successful
        loginPost.done(function() {
            console.log('Login attempt successful, redirecting...')
            window.location.href('/dashboard');
        });
    });
});

// Redirect all authenticated users
function authedUser() {
    window.location.href = '/dashboard';
}