/**
 * Checks if two password strings match.
 * 
 * @param {string} first: The first password string.
 * @param {string} second: The second password string.
 * @param {Element} errorDiv: The div element which will contain any error text
 * to be displayed.
 * @param {Element} errorInput: The input element whose border should be
 * changed to red if the passwords don't match.
 */                      
function checkMatch(first, second, errorDiv, errorInput) {
    // Clear the error text if they match
    if(first === second) {
        errorDiv.empty();
        errorInput.removeClass('error');
    } else {
        // Add the error text
        errorDiv.html('Passwords do not match.');
        errorInput.addClass('error');
    }
}

/**
 * Verifies that an uploaded picture is within the required size limits.
 * 
 * @param {File} file: The picture file to check.
 * @param {Element} error: The div element which will contain any error text to
 * be displayed.
 */
function checkPictureSize(file, error) {
    // Clear the error text
    error.empty();

    // Display error text if too large
    if(file.size > 1000000) {
        console.log('File is too large!');
        error.html('File is too large!');
    }
}