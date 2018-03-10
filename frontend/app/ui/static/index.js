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
        loginPost.fail(function(data) {
            console.log('Login attempt failed.');
            console.log(data);
        });
    });
});