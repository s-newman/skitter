$(document).ready(function() {
    // Check if the passwords match
    $('#second-password').on('input', function(event) {
        // Clear the error text if they match
        if($('#second-password').val() === $('#first-password').val()) {
            $('#error-text').empty();
            $('#second-password').removeClass('error');
        } else {
            // Add the error text
            $('#error-text').html('Passwords do not match.');
            $('#second-password').addClass('error');
        }
    });

    // Detect if file is too big
    $('#picture-upload').bind('change', function() {
        // Clear the error text


        // Display error text if too large
        if(this.files[0].size > 1000000) {
            console.log('File is too large!');
            $('#upload-error-text').html('File is too large!');
        }
    })

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

        // Only allow submission if the passwords match
        if($('#first-password').val() !== $('#second-password').val()) {
            $('#form-error-text').append('Passwords do not match.<br />');
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