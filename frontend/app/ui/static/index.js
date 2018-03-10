// Check if the user is authenticated already
let authCheckPost = $.post('/isAuthenticated', getCookie('SID'), function(data) {
    let response = JSON.parseJSON(data);
    if(response['status'] == 'authenticated') {
        // user is auth'd, redirect em
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

        // Attempt to authenticate
        let loginPost = $.post('/login', postData);

        // Log to console if request failed
        loginPost.fail(function() {
            console.log('Login attempt failed.');
            console.log(postData);
        });

        // Redirect to dashboard page if request was successful
        loginPost.done(function() {
            window.location.href('/dashboard');
        });
    });
});

// Redirect all authenticated users
function authedUser() {
    window.location.href = '/dashboard';
}