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
                event.preventDefault();
            }
        });

        // Log errors from previous request
        usernameGet.fail(function() {
            console.log('Could not check if username ' + $('#username').val() + ' is available.');
            event.preventDefault();
        });
    });

    // Submit profile picture change
    $('#change-profile-pic').submit(function(event) {
        let fileArray = document.getElementById('picture-upload').files;

        // Continue only if the most recently uploaded file is small enough
        if(checkPictureSize(fileArray[fileArray.length - 1].size, $('#upload-error-text'))) {
            console.log('Changing profile picture.');
            
            // Change image
            let putImage = $.put('/changeProfileImage', { place: 'holder'}, function(data) {
                console.log('Successfully changed photo.');
            });

            // Log errors
            putImage.fail(function() {
                console.log('Encountered an error when changing photo.');
                event.preventDefault();
            });
        } else {
            event.preventDefault();
        }
    });
});