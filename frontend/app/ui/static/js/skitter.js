/* A collection of helper functions for Skitter. */

// The location of the default profile picture
var defaultProfile = '/static/img/default-profile.png';

/**
 * Gets the value of a cookie from the browser.
 * @param {string} cname The name of the cookie to get from the browser.
 */
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

/**
 * Adds a cookie to the browser.  Courtesy of w3schools: https://www.w3schools.com/js/js_cookies.asp
 * @param {string} cname The name of the cookie to create
 * @param {string} cvalue The value of the cookie to create
 * @param {number} exdays The number of days the cookie should last
 */
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

/**
 * Makes an AJAX request using the POST method, with an application/json MIME
 * type.
 * @param {string} url The URL to sent the request to
 * @param {string} postData A stringified JSON object to send
 * @param {*} callback The function to run when the request succeeds
 * @param {*} errorCallback The function to run when the request fails
 */
function postJSON(url, postData, callback, errorCallback) {
    jQuery.ajax(url, {
        contentType: 'application/json',
        data: postData,
        error: errorCallback,
        method: 'POST',
        success: callback
    });
}