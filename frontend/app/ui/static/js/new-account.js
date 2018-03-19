$(document).ready(function() {
    // Detect if file is too big
    $('#picture-upload').bind('change', checkPictureSize(
        document.querySelector('#picture-upload').files[0],
        $('#upload-error-text')));

    // Create the new user
    $('#new-acct-form').submit(function(event) {
        // Track whether there were any errors
        let error = false;

        // Clear the error text
        $('#form-error-text').empty();

        // Check if all forms have been filled
        if($('#username').val() === '' ||
           $('#first-password').val() === '' ||
           $('#second-password').val() === '' ||
           $('#picture-upload').val() === '' ||
           $('#email').val() === '') {
            console.log('Not all form fields are filled.');
            $('#form-error-text').html('Please fill out all form fields!<br />');
            error = true;
            event.preventDefault();
        }

        // Only allow submission if the file is small enough
        try {
            // Attempt the thing
            if(document.getElementById('picture-upload').files[0].size > 1000000) {
                $('#form-error-text').append('File upload is too large.');
                event.preventDefault();
                error = true;
            }
        } catch (e) {
            // Handle the exception if no file has been uploaded
            if(e instanceof TypeError) {
                $('#form-error-text').append('Please upload a profile picture.');
                event.preventDefault();
                error = true;
            } else {
                // This shouldn't happen, let it bubble
                throw e;
            }
        }

        // Display information if there were any problems
        if(error) {
            console.log('Please resolve errors.');
            $('#form-error-text').prepend('Please correct the following errors:<br />');
        }

        // Allow the form to be submitted
    });
});