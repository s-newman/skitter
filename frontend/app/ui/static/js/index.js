$(document).ready(function () {
    // Attempt to log in the user when they submit the login form
    $('#loginForm').submit(function(event) {
        // Clear error
        $('#errorText').empty();
        $('#username').css('border-color', '#6c3c17');
        $('#password').css('border-color', '#6c3c17');
        
        // Create JSON string to send
        let postData = {
            username: $('#username').val(),
            password: $('#password').val()
        };
        console.log('Attempting to authenticate user:', postData);

        // Attempt to authenticate
        let loginPost = $.post('/signIn', postData);

        // Log to console if request failed
        loginPost.fail(function() {
            // Display error to user
            $('#errorText').html('Invalid credentials.');
            $('#username').css('border-color', '#ff0000');
            $('#password').css('border-color', '#ff0000');
            console.log('Login attempt failed.');
        });

        // Redirect to dashboard page if request was successful
        loginPost.done(function() {
            console.log('Login attempt successful, redirecting...')
            authedUser();
        });
        event.preventDefault();
    });
});

// Redirect all authenticated users
function authedUser() {
    window.location.href = '/dashboard';
}