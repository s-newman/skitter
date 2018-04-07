$(document).ready(function() {
    // Create the user
    $('#accept').click(function() {
        console.log('Hooray!');
        
        // Create the data to send
        let postData = JSON.stringify({
            rit_username: getCookie('username'),
            firstname: getCookie('firstname'),
            lastname: getCookie('lastname')
        });

        // Create the user
        let newUserRequest = $.ajax({
            type: 'POST',
            url: '/newUser',
            contentType: 'application/json',
            data: postData
        });

        // Successful request was made
        newUserRequest.done(function(data) {
            if(data.successful === 'true') {
                // User was created
                console.log('Created user.');
                window.location.href = '/dashboard';
            } else {
                // User was not created
                console.log('An error occurred.');
                window.location.href = '/logout';
            }
        });

        // This shouldn't happen but it did
        newUserRequest.fail(function() {
            console.log('A request failure occurred.  This should not happen.');
            window.location.href = '/logout';
        });
    })

    // Don't create a user
    $('#deny').click(function() {
        console.log('Fine then, jeez.');
        window.location.href = '/logout';
    })
});