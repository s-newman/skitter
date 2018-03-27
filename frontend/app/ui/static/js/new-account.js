$(document).ready(function() {
    // Create the new user
    $('#new-acct-form').submit(function(event) {
        // Clear the error text
        $('#form-error-text').empty();

        // Check if all forms have been filled
        if($('#username').val() === '') {
            console.log('The username has not been entered.');
            $('#form-error-text').html('Please pick a username!<br />');
            event.preventDefault();
        }
        // Allow the form to be submitted
    });
});