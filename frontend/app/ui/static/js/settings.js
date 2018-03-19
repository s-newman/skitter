/**
 * Verifies that an uploaded picture is within the required size limits.
 * 
 * @param {File} file: The picture file to check.
 * @param {Element} error: The div element which will contain any error text to
 * be displayed.
 * @returns {boolean}: True if the file is within the limits, false if the file
 * is too large.
 */
function checkPictureSize(file, error) {
    // Clear the error text
    error.empty();

    // Display error text if too large
    if(file.size > 1000000) {
        console.log('File is too large!');
        error.html('File is too large!');
        return false;
    } else {
        // File is small enough
        return true;
    }
}